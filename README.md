# 💰 TabunganKu - Aplikasi Manajemen Tabungan

Aplikasi manajemen tabungan dengan fitur deteksi uang menggunakan kamera (AI-powered).

## 🎯 Fitur Utama

### ✅ Fitur yang Sudah Diimplementasikan

1. **Splash Screen**
   - Tampilan awal dengan animasi fade
   - Auto-redirect ke halaman login

2. **Login**
   - UI modern dengan gradient background
   - Form validation
   - Default credentials: admin/admin

3. **Dashboard dengan Tab Navigation**
   - **Tab Tabungan Aktif**: Menampilkan daftar tabungan yang masih berjalan
   - **Tab Riwayat Bongkar**: Menampilkan tabungan yang sudah dibongkar
   - Tab aktif akan ter-disable (grayed out)

4. **CRUD Tabungan**
   - ✅ **Create**: Buat tabungan baru dengan nama, target, dan mata uang
   - ✅ **Read**: Tampilkan list tabungan dengan pagination (10 item/halaman)
   - ✅ **Update**: Edit nama, target, dan mata uang tabungan
   - ✅ **Delete**: Hapus tabungan beserta semua riwayatnya

5. **Detail Tabungan (Modal)**
   - Menampilkan total tabungan terkumpul
   - Progress bar dengan persentase
   - Sisa target yang harus dicapai
   - Button **Menabung** untuk menambah uang
   - Button **Bongkar** untuk memindahkan ke riwayat
   - List riwayat menabung dengan pagination (10 item/halaman)

6. **Fitur Menabung**
   - Modal kamera (simulasi)
   - Input manual nominal uang
   - Notifikasi setelah berhasil menabung
   - Auto-update total dan progress

7. **Fitur Bongkar**
   - Konfirmasi sebelum membongkar
   - Memindahkan tabungan ke tab "Riwayat Bongkar"
   - Status berubah dari 'active' menjadi 'broken'

### 🚧 Fitur yang Akan Dikembangkan

- **AI Money Detection**: Deteksi denominasi uang kertas menggunakan kamera
- **Multiple Currency Detection**: Deteksi berbagai mata uang
- **Real-time Camera Feed**: Streaming kamera langsung di browser
- **Toast Notifications**: Notifikasi modern menggantikan alert()

## 🛠️ Teknologi yang Digunakan

### Frontend
- **Vue 3** (Composition API)
- **Vite** (Build tool & dev server)
- **Tailwind CSS** (Styling)
- **Axios** (HTTP client)
- **Vue Router** (Navigation)

### Backend
- **FastAPI** (Python web framework)
- **SQLAlchemy** (ORM)
- **MySQL** (Database)
- **Uvicorn** (ASGI server)
- **PyMySQL** (MySQL driver)

## 📦 Instalasi

### 1. Clone Repository
```bash
git clone <repository-url>
cd tabungan-ku
```

### 2. Setup Backend

```bash
# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment
# Windows:
.\venv\Scripts\Activate.ps1
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install fastapi sqlalchemy pymysql uvicorn python-dotenv

# Setup database MySQL
# Buat database 'tabungan_db' di MySQL
# Update koneksi di database.py jika perlu
```

### 3. Setup Frontend

```bash
cd tabungan-ku

# Install dependencies
npm install

# Jalankan dev server
npm run dev
```

## 🚀 Menjalankan Aplikasi

### Terminal 1: Backend (FastAPI)
```bash
# Di root folder (tabungan-ku/)
.\venv\Scripts\Activate.ps1
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### Terminal 2: Frontend (Vite)
```bash
# Di folder tabungan-ku/tabungan-ku/
npm run dev
```

Aplikasi akan berjalan di:
- **Frontend**: http://localhost:5173 (atau 5174 jika port 5173 terpakai)
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 📁 Struktur Database

### Tabel: `users`
| Field    | Type    | Description        |
|----------|---------|-------------------|
| id       | INT     | Primary key       |
| username | VARCHAR | Username login    |
| password | VARCHAR | Password login    |

### Tabel: `saving_plans`
| Field         | Type    | Description                    |
|---------------|---------|-------------------------------|
| id            | INT     | Primary key                   |
| user_id       | INT     | Foreign key ke users          |
| name          | VARCHAR | Nama tabungan                 |
| target_amount | FLOAT   | Target nominal                |
| currency      | VARCHAR | Mata uang (IDR/USD)          |
| status        | VARCHAR | active/broken                 |
| created_at    | DATETIME| Waktu dibuat                  |

### Tabel: `saving_logs`
| Field      | Type    | Description                    |
|------------|---------|-------------------------------|
| id         | INT     | Primary key                   |
| plan_id    | INT     | Foreign key ke saving_plans   |
| amount     | FLOAT   | Nominal yang ditabung         |
| created_at | DATETIME| Waktu menabung                |

## 🔌 API Endpoints

### Plans
- `GET /plans/{user_id}` - Ambil semua tabungan user
- `POST /plans/create` - Buat tabungan baru
- `PUT /plans/edit/{plan_id}` - Edit tabungan
- `DELETE /plans/{plan_id}` - Hapus tabungan
- `PUT /plans/bongkar/{plan_id}` - Bongkar tabungan

### Saving
- `POST /plans/{plan_id}/save` - Tambah uang ke tabungan
- `GET /plans/{plan_id}/logs` - Ambil riwayat tabungan

## 🎨 Skenario Penggunaan

### 1. Login
- Buka aplikasi
- Tunggu splash screen (2.5 detik)
- Masukkan username: `admin`
- Masukkan password: `admin`
- Klik "Masuk"

### 2. Buat Tabungan Baru
- Klik button "+ Buat Tabungan"
- Isi nama (contoh: "Beli Motor")
- Pilih mata uang (IDR/USD)
- Isi target nominal (contoh: 20000000)
- Klik "Buat Sekarang"

### 3. Menabung
- Klik list tabungan yang ingin ditabung
- Pada modal detail, klik button "Menabung"
- Masukkan nominal uang (contoh: 500000)
- Klik "Simpan"
- Lihat notifikasi dan progress terupdate

### 4. Lihat Detail & Riwayat
- Klik list tabungan
- Modal akan menampilkan:
  - Total terkumpul
  - Sisa target
  - Progress bar
  - Riwayat menabung (dengan pagination)

### 5. Edit Tabungan
- Klik icon 3 titik (⋮) di list tabungan
- Pilih "Edit"
- Ubah nama/target/mata uang
- Klik "Simpan"

### 6. Bongkar Tabungan
- Buka detail tabungan
- Klik button "Bongkar"
- Konfirmasi
- Tabungan akan pindah ke tab "Riwayat Bongkar"

### 7. Hapus Tabungan
- Klik icon 3 titik (⋮) di list tabungan
- Pilih "Hapus"
- Konfirmasi
- Tabungan dan semua riwayatnya akan terhapus

## 🐛 Troubleshooting

### Backend tidak bisa connect ke database
```python
# Cek koneksi di database.py
DATABASE_URL = "mysql+pymysql://root:@localhost/tabungan_db"

# Pastikan MySQL service berjalan
# Pastikan database 'tabungan_db' sudah dibuat
```

### Frontend error CORS
```python
# Pastikan CORS sudah dikonfigurasi di main.py:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Port 5173 sudah terpakai
```bash
# Vite otomatis akan mencoba port lain (5174, 5175, dst)
# Atau matikan aplikasi yang menggunakan port tersebut
```

## 👨‍💻 Developer

Tugas Besar - Pengantar AI
Tahun Ajaran 2025/2026
