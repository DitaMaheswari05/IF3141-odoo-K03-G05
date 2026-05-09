# Plumeria Cafe & Creative Space — Sistem Informasi Operasional
**IF3141 Sistem Informasi | Kelompok 05 Kelas K03**

> Anggota: Attara Majesta Ayub · Dita Maheswari · Jovandra Otniel P.S. · M. Abizzar Gamadrian · Anas Ghazi Al Gifari

---

## Daftar Isi

1. [Tentang Proyek](#tentang-proyek)
2. [Prasyarat](#prasyarat)
3. [Struktur Direktori](#struktur-direktori)
4. [Instalasi Pertama Kali](#instalasi-pertama-kali)
5. [Menjalankan Setelah Instalasi](#menjalankan-setelah-instalasi)
6. [Update Modul Setelah Perubahan Kode](#update-modul-setelah-perubahan-kode)
7. [Membuat Akun Demo per Role](#membuat-akun-demo-per-role)
8. [Migrasi Database (Export / Import)](#migrasi-database-export--import)
9. [Troubleshooting](#troubleshooting)

---

## Tentang Proyek

Modul custom Odoo 17 untuk sistem informasi operasional **Plumeria Cafe & Creative Space**, Jl. Cikuda No. 37, Jatinangor. Sistem ini mencakup:

| Fitur | Functional Requirement |
|---|---|
| Login & autentikasi berbasis peran (RBAC) | FR-06 |
| Input laporan operasional harian + workflow validasi | FR-01, FR-05 |
| Import & input data transaksi POS | FR-02 |
| Dashboard performa bisnis (QWeb custom) | FR-03 |
| Analisis produk unggulan & promo | FR-04 |
| Rekap keuangan & rekonsiliasi harian | FR-05, FR-06 |

---

## Prasyarat

Pastikan software berikut sudah terpasang sebelum memulai:

| Software | Keterangan | Link |
|---|---|---|
| **Docker Desktop** | Wajib — menjalankan Odoo & PostgreSQL | https://www.docker.com/products/docker-desktop/ |
| **Git** | Untuk clone & kolaborasi repo | https://git-scm.com/ |
| **Python 3.11** | Opsional — untuk virtual environment lokal | https://www.python.org/downloads/ |

> **Catatan:** Pastikan Docker Desktop sudah **berjalan** (ikon Docker muncul di system tray) sebelum menjalankan perintah apapun.

---

## Struktur Direktori

```
IF3141-odoo-K03-G05/
├── config/                  # Konfigurasi Odoo (odoo.conf)
├── custom_addons/
│   └── plumeria_cafe/       # Modul custom utama
│       ├── models/          # Model data (Python)
│       ├── views/           # Tampilan (XML + QWeb)
│       ├── security/        # RBAC: grup & access control
│       ├── data/            # Sequence & demo data
│       └── controllers/     # Controller HTTP (dashboard)
├── dump/                    # Hasil export database (.sql)
├── scripts/                 # Script export & import database
│   ├── export_db.sh / .cmd
│   └── import_db.sh / .cmd
└── docker-compose.yml       # Orchestration Docker
```

---

## Instalasi Pertama Kali

> Ikuti section ini **hanya jika belum pernah menjalankan** proyek ini sama sekali di komputer kamu.

### Langkah 1 — Clone Repository

```bash
git clone <url-repo>
cd IF3141-odoo-K03-G05
```

### Langkah 2 — Jalankan Docker

```bash
docker compose up -d
```

Perintah ini akan mengunduh image Odoo 17 dan PostgreSQL lalu menjalankannya di background. Proses download membutuhkan waktu beberapa menit pada percobaan pertama.

**Cek apakah container sudah berjalan:**

```bash
docker compose ps
```

Output yang diharapkan — kolom `Status` menunjukkan `running`:

```
NAME        STATUS
odoo-web    running
odoo-db     running
```

**Pantau log jika ingin melihat progress startup:**

```bash
docker compose logs -f web
```

Tunggu hingga muncul baris seperti:
```
INFO odoo odoo.service.server: HTTP service (werkzeug) running on 0.0.0.0:8069
```
Lalu tekan `Ctrl+C` untuk keluar dari log.

### Langkah 3 — Buat Database Odoo

1. Buka browser dan akses: **http://localhost:8069**
2. Kamu akan melihat halaman **"Create Database"**. Isi sebagai berikut:

   | Field | Nilai |
   |---|---|
   | Master Password | *(kosongkan)* |
   | Database Name | `plumeria_db` |
   | Email | `admin@plumeria.com` |
   | Password | `admin` |
   | Language | English atau Bahasa Indonesia |
   | Country | Indonesia |
   | Demo data | **JANGAN dicentang** |

3. Klik **"Create Database"** dan tunggu hingga proses selesai (1-3 menit).

### Langkah 4 — Aktifkan Developer Mode

1. Login dengan email `admin@plumeria.com` dan password `admin`
2. Buka **Settings** (menu kiri)
3. Scroll ke bawah → klik **"Activate the developer mode"**
4. Halaman akan reload secara otomatis

### Langkah 5 — Update Daftar Aplikasi

1. Klik menu **Apps** di navbar atas
2. Klik **"Update Apps List"** (ada di bagian atas halaman)
3. Klik **"Update"** pada dialog konfirmasi

### Langkah 6 — Install Modul Plumeria Cafe

1. Di halaman **Apps**, hapus filter "Apps" yang aktif
2. Cari: `Plumeria`
3. Temukan **"Plumeria Cafe & Creative Space"**, klik **"Install"**
4. Tunggu proses instalasi selesai (~1 menit)

Setelah install, menu **"Plumeria Cafe"** akan muncul di navbar. Demo data (produk, transaksi 5 hari, laporan) sudah otomatis ter-load.

### Langkah 7 (Opsional) — Setup Virtual Environment Lokal

Hanya diperlukan jika IDE kamu perlu mengenali package Odoo untuk autocomplete:

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```

---

## Menjalankan Setelah Instalasi

> Gunakan section ini untuk **penggunaan sehari-hari** setelah instalasi pertama selesai.

### Menjalankan Odoo

```bash
docker compose up -d
```

Lalu buka **http://localhost:8069** dan login.

### Menghentikan Odoo

```bash
docker compose down
```

> Selalu jalankan perintah ini sebelum mematikan komputer agar database tidak corrupt.

### Melihat Log (jika ada error)

```bash
docker compose logs -f web
```

### Restart Odoo (jika hang atau perlu refresh)

```bash
docker compose restart web
```

---

## Update Modul Setelah Perubahan Kode

Setiap kali ada perubahan pada file Python (models) atau XML (views, security), modul perlu di-upgrade agar perubahan terapply ke database.

### Cara 1 — Via Odoo UI (Direkomendasikan)

1. Pastikan Docker sudah berjalan
2. Buka **http://localhost:8069** → login sebagai admin
3. Buka menu **Apps**
4. Hapus filter "Apps", cari `Plumeria`
5. Klik tombol **"Upgrade"** (bukan Install)

### Cara 2 — Via Command Line

```bash
docker compose exec web odoo -u plumeria_cafe -d plumeria_db \
  --db_host=db --db_port=5432 --db_user=odoo --db_password=password \
  --stop-after-init
```

Setelah selesai, jalankan kembali:

```bash
docker compose restart web
```

> **Kapan perlu upgrade?**
> - Menambah/mengubah field pada model (`.py`)
> - Mengubah file `security/groups.xml` atau `ir.model.access.csv`
> - Menambah/mengubah data di folder `data/`
>
> **Tidak perlu upgrade:**
> - Mengubah tampilan views (`.xml`) — cukup restart Odoo
> - Mengubah controller Python — cukup restart Odoo

---

## Membuat Akun Demo per Role

Setelah modul terinstall, buat user Odoo untuk setiap role agar bisa demo RBAC. Lakukan di **Settings → Users & Companies → Users**.

| Nama | Email Login | Password | Grup Plumeria |
|---|---|---|---|
| Irad (Op. Coordinator) | `opcoord@plumeria.com` | `plumeria123` | Operational Coordinator |
| Finance Staff | `finance@plumeria.com` | `plumeria123` | Finance |
| Head Kitchen | `hkitchen@plumeria.com` | `plumeria123` | Head Kitchen |
| Head Bar | `hbar@plumeria.com` | `plumeria123` | Head Bar |
| Marketing Staff | `marketing@plumeria.com` | `plumeria123` | Marketing |

> **Catatan:** User `admin` sudah otomatis masuk grup **Head of Operations** saat modul diinstall.

**Cara assign grup:**
1. Buka user yang baru dibuat
2. Scroll ke bagian **"Plumeria Cafe"**
3. Pilih role yang sesuai dari dropdown
4. Klik **"Save"**

---

## Migrasi Database (Export / Import)

Database Odoo bersifat lokal. Gunakan script ini untuk berbagi state database antar anggota tim.

> **WAJIB:** Matikan Odoo dulu sebelum export/import.

```bash
docker compose down
```

### Export Database (sebelum push ke repo)

- **Windows:**
  ```bat
  scripts\export_db.cmd
  ```
- **macOS/Linux:**
  ```bash
  ./scripts/export_db.sh
  ```

File hasil export akan tersimpan di folder `dump/`.

### Import Database (setelah pull dari repo)

- **Windows:**
  ```bat
  scripts\import_db.cmd
  ```
- **macOS/Linux:**
  ```bash
  ./scripts/import_db.sh
  ```

Setelah import selesai, jalankan kembali:

```bash
docker compose up -d
```

---

## Troubleshooting

### Odoo tidak bisa diakses di localhost:8069

```bash
# Cek apakah container berjalan
docker compose ps

# Lihat log error
docker compose logs web --tail=50
```

Jika container tidak berjalan, coba:
```bash
docker compose down
docker compose up -d
```

### Error "modul tidak ditemukan" saat install

Pastikan path di `docker-compose.yml` sudah benar:
```yaml
volumes:
  - ./custom_addons:/mnt/extras-addons
```
Lalu restart dan update apps list ulang.

### Perubahan kode tidak terapply

Coba sequence berikut:
```bash
docker compose restart web
```
Jika masih belum, lakukan **Upgrade** modul via Odoo UI.

### Database corrupt / error setelah force-shutdown

Restore dari backup terakhir di folder `dump/` menggunakan script import.

### Port 8069 sudah dipakai proses lain

Edit `docker-compose.yml`, ubah mapping port:
```yaml
ports:
  - "8070:8069"   # ganti 8070 dengan port lain
```
Lalu akses via **http://localhost:8070**.
