-- Tambah kolom broken_at untuk mencatat waktu bongkar tabungan
USE tabungan_db;

ALTER TABLE saving_plans 
ADD COLUMN broken_at DATETIME NULL 
AFTER status;

-- Verifikasi struktur tabel
DESCRIBE saving_plans;
