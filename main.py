from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from database import SessionLocal, SavingPlan, SavingLog, User
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import datetime
import io
from PIL import Image
import numpy as np
import cv2
from ultralytics import YOLO

app = FastAPI()

# WAJIB: Agar Frontend bisa akses Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Di produksi nanti ganti dengan URL frontendmu
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load YOLO model (ganti path sesuai lokasi best.pt Anda)
# Contoh path: "best.pt" jika file di folder yang sama dengan main.py
# Atau: "runs/detect/train/weights/best.pt" jika di folder training
try:
    model = YOLO("best.pt")  # Ganti dengan path file best.pt Anda
    print("✅ YOLO model loaded successfully!")
    print(f"📋 Class names: {model.names}")
except Exception as e:
    print(f"❌ Error loading YOLO model: {e}")
    model = None

# Dependency untuk koneksi database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Schema Data (Pydantic) - Agar input user tervalidasi
class PlanCreate(BaseModel):
    user_id: int
    name: str
    target_amount: float
    currency: str
    duration_days: int

# --- ENDPOINT DASHBOARD ---

@app.get("/plans/{user_id}")
def get_plans(user_id: int, db: Session = Depends(get_db)):
    # Mengambil list tabungan yang masih AKTIF
    active = db.query(SavingPlan).filter(SavingPlan.user_id == user_id, SavingPlan.status == 'active').all()
    # Mengambil list tabungan yang sudah DIBONGKAR
    broken = db.query(SavingPlan).filter(SavingPlan.user_id == user_id, SavingPlan.status == 'broken').all()
    
    return {
        "active_plans": active,
        "history_plans": broken
    }

@app.post("/plans/create")
def create_plan(plan: PlanCreate, db: Session = Depends(get_db)):
    new_plan = SavingPlan(
        user_id=plan.user_id,
        name=plan.name,
        target_amount=plan.target_amount,
        currency=plan.currency,
        status="active"
    )
    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)
    return {"message": "Tabungan berhasil dibuat", "data": new_plan}

@app.put("/plans/bongkar/{plan_id}")
def bongkar_tabungan(plan_id: int, db: Session = Depends(get_db)):
    plan = db.query(SavingPlan).filter(SavingPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Tabungan tidak ditemukan")
    
    plan.status = "broken" # Pindah ke riwayat bongkar
    plan.broken_at = datetime.datetime.now()  # Catat waktu bongkar
    db.commit()
    return {"message": "Tabungan berhasil dibongkar!"}

# Schema untuk update plan
class PlanUpdate(BaseModel):
    name: str | None = None
    target_amount: float | None = None
    currency: str | None = None

@app.put("/plans/edit/{plan_id}")
def edit_plan(plan_id: int, plan_update: PlanUpdate, db: Session = Depends(get_db)):
    plan = db.query(SavingPlan).filter(SavingPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Tabungan tidak ditemukan")
    
    if plan_update.name:
        plan.name = plan_update.name
    if plan_update.target_amount:
        plan.target_amount = plan_update.target_amount
    if plan_update.currency:
        plan.currency = plan_update.currency
    
    db.commit()
    db.refresh(plan)
    return {"message": "Tabungan berhasil diupdate", "data": plan}

@app.delete("/plans/{plan_id}")
def delete_plan(plan_id: int, db: Session = Depends(get_db)):
    plan = db.query(SavingPlan).filter(SavingPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Tabungan tidak ditemukan")
    
    # Hapus semua log tabungan terkait
    db.query(SavingLog).filter(SavingLog.plan_id == plan_id).delete()
    # Hapus plan
    db.delete(plan)
    db.commit()
    return {"message": "Tabungan berhasil dihapus"}

# Schema untuk menabung
class SavingAdd(BaseModel):
    amount: float

@app.post("/plans/{plan_id}/save")
def add_saving(plan_id: int, saving: SavingAdd, db: Session = Depends(get_db)):
    plan = db.query(SavingPlan).filter(SavingPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Tabungan tidak ditemukan")
    
    # Tambah log tabungan
    new_log = SavingLog(
        plan_id=plan_id,
        amount=saving.amount
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    
    # Hitung total tabungan
    total = db.query(SavingLog).filter(SavingLog.plan_id == plan_id).all()
    total_amount = sum([log.amount for log in total])
    
    return {
        "message": "Berhasil menabung!",
        "saved_amount": saving.amount,
        "total_saved": total_amount,
        "target": plan.target_amount,
        "remaining": plan.target_amount - total_amount
    }

@app.get("/plans/{plan_id}/logs")
def get_saving_logs(plan_id: int, db: Session = Depends(get_db)):
    plan = db.query(SavingPlan).filter(SavingPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Tabungan tidak ditemukan")
    
    logs = db.query(SavingLog).filter(SavingLog.plan_id == plan_id).order_by(SavingLog.created_at.desc()).all()
    
    # Hitung total
    total_amount = sum([log.amount for log in logs])
    
    return {
        "plan": plan,
        "logs": logs,
        "total_saved": total_amount,
        "target": plan.target_amount,
        "remaining": plan.target_amount - total_amount,
        "progress_percentage": (total_amount / plan.target_amount * 100) if plan.target_amount > 0 else 0
    }

# --- ENDPOINT AI DETECTION ---
@app.post("/detect")
async def detect_banknotes(image: UploadFile = File(...)):
    """
    Deteksi uang kertas Rupiah menggunakan YOLOv8 model
    """
    try:
        # Validasi model loaded
        if model is None:
            raise HTTPException(status_code=503, detail="Model YOLO belum dimuat. Pastikan file best.pt ada.")
        
        # Validasi file image
        if not image.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File harus berupa gambar")
        
        # Baca dan konversi image
        contents = await image.read()
        img = Image.open(io.BytesIO(contents))
        img_array = np.array(img)
        
        # Convert RGB to BGR (YOLO expects BGR)
        if len(img_array.shape) == 3 and img_array.shape[2] == 3:
            img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        else:
            img_bgr = img_array
        
        # Run YOLO detection
        results = model(img_bgr, conf=0.5)  # Confidence threshold 0.5
        
        detected_banknotes = []
        
        # Parse detection results
        for result in results:
            boxes = result.boxes
            
            for box in boxes:
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                class_name = model.names[class_id]
                
                # Convert class name to nominal value
                # Asumsi class name = "10000", "50000", dll
                try:
                    denomination = int(class_name)
                    
                    detected_banknotes.append({
                        "value": denomination,
                        "confidence": round(confidence, 2),
                        "currency": "IDR"
                    })
                except ValueError:
                    # Skip jika class name bukan angka
                    print(f"⚠️ Class name '{class_name}' bukan nominal valid, dilewati.")
                    continue
        
        # Hitung total (akumulasi jika lebih dari 1 lembar)
        total_amount = sum([note["value"] for note in detected_banknotes])
        
        # Response
        if len(detected_banknotes) > 0:
            return {
                "success": True,
                "message": f"Berhasil mendeteksi {len(detected_banknotes)} lembar uang",
                "banknotes": detected_banknotes,
                "total": total_amount,
                "count": len(detected_banknotes),
                "image_size": {"width": img.width, "height": img.height}
            }
        else:
            return {
                "success": False,
                "message": "Tidak ada uang terdeteksi",
                "banknotes": [],
                "total": 0,
                "count": 0,
                "image_size": {"width": img.width, "height": img.height}
            }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error in detection: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")