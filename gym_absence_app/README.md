# 🏋️ Nivans Gym — Sistem Absensi & Keanggotaan Member

Aplikasi desktop manajemen absensi dan membership gym modern berbasis **Python**, **SQLite**, dan **CustomTkinter** dengan styling Dark Mode modern sesuai doktrin **AI Garnet** & **Nivansware**.

---

## 💎 Fitur Utama & Kepatuhan Spesifikasi

1. **Pendaftaran Member (Rule 1 & 2)**:
   - Form biodata lengkap: Nama Lengkap, Jenis Kelamin (Laki-laki/Perempuan), Alamat, Nomor HP.
   - Pilihan paket dalam 1 bulan:
     - 🏋️ **Class Program**: Latihan bersama coach gym, dibatasi **maksimal 8 kali absensi** dalam masa aktif 1 bulan.
     - 💪 **Open Gym**: Bebas absensi setiap hari selama masa aktif 1 bulan.
   - Penomoran ID Member otomatis dimulai dari `001`, `002`, ... `999`, lalu bertransisi ke `1000`, `1001`, dst.
2. **Kalkulasi Status Dinamis (Rule 3)**:
   - Status terbagi 2: **Active** dan **Non-Active**.
   - Status dihitung dinamis:
     - **Open Gym**: Active jika tanggal daftar/perpanjangan < 1 bulan (30 hari).
     - **Class**: Active jika masa aktif < 1 bulan DAN kuota sesi belum habis (< 8 sesi). Jika sudah mencapai 8 sesi, status menjadi `Non-Active (Kuota 8/8 Habis)`.
   - Kolom khusus `Kuota / Sesi` di tabel member menampilkan progres kehadiran (misal `3/8 Sesi` atau `Unlimited`).
3. **Presensi Cepat dengan Nomor ID (Rule 4 & 5)**:
   - Input nomor ID lalu klik tombol kehadiran (Warna Primer `#c00707`).
   - Pop-up modal muncul dengan notifikasi resmi: `"Anda berhasil absen pada hari ini"`.
   - **Validasi 1x Absen per Hari**: Sistem menolak absensi ganda jika member sudah absen di hari yang sama, lengkap dengan informasi jam absensi sebelumnya.
   - Setelah notifikasi ditutup, otomatis kembali ke halaman utama / form absensi siap pakai.
4. **Kalender Tanda Absensi Member**:
   - Tombol `📅 Kalender Absensi` di panel data member.
   - Menampilkan visual kalender bulanan interaktif dengan tanda checklist/badge kehadiran di tanggal member hadir beserta jam kehadiran (`✓ HH:MM`), navigasi bulan, dan total kehadiran.
5. **Dashboard & Grafik Pengunjung (Fitur Baru - Premium SaaS)**:
   - Tab navigasi `📊 Statistik & Grafik`.
   - **4 Bento KPI Cards**: Total Kunjungan Hari Ini, Rata-rata Harian Mingguan, Jam Teramai (Peak Hours), dan Member Teraktif.
   - **Grafik Batang Vektor Berkecepatan Tinggi (Native Canvas 60 FPS)**: Histogram tren kunjungan 7 hari terakhir dengan sudut membulat (*rounded bars*), otomatis menonjolkan hari puncak (*peak day*) dengan warna emas `#df9e12`.
   - **Distribusi Paket**: Analisis rasio kunjungan member paket Open Gym vs Class Program.
   - **Statistik Keanggotaan**: Status proporsi member Active vs Non-Active.
6. **Panel Admin & Perpanjangan (Rule 6)**:
   - Admin dapat memperpanjang masa aktif paket member yang telah kedaluwarsa (+1 bulan / 30 hari).
7. **Penghapusan Aman (Rule 7)**:
   - Admin hanya dapat menghapus member yang berstatus **Non-Active**. Member yang masih **Active** diproteksi dari penghapusan tidak sengaja.
8. **Pencarian Instan (Rule 8)**:
   - Pencarian real-time berdasarkan **Nomor ID** maupun **Nama Member**.
7. **Clean Code & Layered Architecture (Rule 9)**:
   - Pemisahan tanggung jawab (*Separation of Concerns*):
     - `domain/`: Business entities & custom exceptions.
     - `infrastructure/`: SQLite connection manager & repository pattern.
     - `application/`: Service layer use cases.
     - `presentation/`: Modern CustomTkinter UI, theme tokens, dan modal dialogs.
     - `tests/`: TDD Unit test suite mencakup 100% logika bisnis.
8. **Eksekusi Sekali Klik / .EXE Standalone (Rule 10)**:
   - Disertakan `run_app.bat` untuk menjalankan langsung tanpa terminal.
   - Disertakan `build_exe.bat` untuk membungkus aplikasi menjadi file `.exe`.

---

## 🎨 Visual Design Tokens

- **Primary Colour**: `#c00707` (Crimson / Wine Red)
- **Secondary Colour**: `#df9e12` (Amber Gold)
- **Dark Mode BG**: `#292929` (Charcoal)
- **Surface Cards**: `#343434` / `#1f1f1f`
- **Typography**: Modern Segoe UI Clean Font

---

## 🚀 Cara Menjalankan

### Opsi 1: Menjalankan Langsung via File Batch
Cukup klik ganda pada file:
```
run_app.bat
```

### Opsi 2: Menjalankan via Terminal
```bash
cd d:\Nivansware\Test-mini_project\gym_absence_app
python main.py
```

### Opsi 3: Membangun Executable .EXE
Jalankan file:
```
build_exe.bat
```
File executable `.exe` mandiri akan tersedia di folder `dist\NivansGymApp\NivansGymApp.exe`.
