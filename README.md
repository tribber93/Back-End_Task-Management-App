# Task Management App - Backend

## Deskripsi

Backend untuk Task Management App dikembangkan menggunakan FastAPI dan dideploy menggunakan AWS EC2. Backend ini menyediakan layanan autentikasi pengguna dan manajemen tugas. untuk dokumen melalui Swagger UI bisa diakses [https://api.tribber.live/docs](https://api.tribber.live/docs)

## Fitur

- **Autentikasi Pengguna**:
  - Sign up
  - Sign in
  - Logout
  - Mendapatkan data pengguna
  - Menghapus akun
- **Manajemen Tugas**:
  - Mendapatkan daftar tugas pengguna
  - Membuat tugas baru
  - Memperbarui tugas
  - Menghapus tugas

## Endpoint API

### Autentikasi

- `POST /api/v1/auth/signup` - Mendaftarkan pengguna baru
- `POST /api/v1/auth/signin` - Login pengguna
- `GET /api/v1/auth/me` - Mendapatkan data pengguna saat ini
- `GET /api/v1/auth/logout` - Logout pengguna
- `DELETE /api/v1/auth/delete` - Menghapus akun pengguna

### Manajemen Tugas

- `GET /api/v1/task/get` - Mendapatkan daftar tugas pengguna
- `POST /api/v1/task/create` - Membuat tugas baru
- `PUT /api/v1/task/update/{task_id}` - Memperbarui tugas berdasarkan ID
- `DELETE /api/v1/task/delete/{task_id}` - Menghapus tugas berdasarkan ID

## Teknologi yang Digunakan

- **Backend**: FastAPI
- **Database**: Supabase
- **Deployment**: AWS EC2
- **Containerization**: Docker & Docker Compose

## Instalasi dan Menjalankan Backend

### Prasyarat

Pastikan Anda sudah menginstal:

- Python 3.9+
- Pip
- Virtualenv (opsional, tetapi disarankan)
- Docker & Docker Compose

Siapkan file `.env` yang memiliki value seperti pada .env.local

### Menjalankan Secara Lokal tanpa Docker

1. Clone repository ini:
   ```bash
   git clone https://github.com/tribber93/Back-End_Task-Management-App.git
   cd Back-End_Task-Management-App
   ```
2. Buat virtual environment dan aktifkan:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Untuk macOS/Linux
   venv\Scripts\activate    # Untuk Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Jalankan server FastAPI:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```
5. Backend akan berjalan di `http://localhost:8000`

### Menjalankan Secara Lokal dengan Docker Compose

1. Jalankan aplikasi dengan Docker Compose:
   ```bash
   docker-compose up --build -d
   ```
2. Backend akan berjalan di `http://localhost:8000`
