from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

# Ganti sesuai settingan MySQL kamu
DATABASE_URL = "mysql+pymysql://root:@localhost/tabungan_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)
    password = Column(String(100))

class SavingPlan(Base):
    __tablename__ = "saving_plans"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(100))
    target_amount = Column(Float)
    currency = Column(String(10)) # IDR atau USD
    status = Column(String(20), default="active") # active / broken
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    broken_at = Column(DateTime, nullable=True)  # Waktu dibongkar

class SavingLog(Base):
    __tablename__ = "saving_logs"
    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("saving_plans.id"))
    amount = Column(Float)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# Perintah untuk membuat tabel otomatis
def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Database & Tabel Berhasil Dibuat!")