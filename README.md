# 📝 Analisis Sentimen Layanan SAMSAT

Aplikasi ini merupakan sistem input komentar publik dan dashboard admin untuk melakukan **analisis sentimen terhadap layanan SAMSAT** berbasis platform media sosial.

---

## 📌 Fitur Utama

### 🧾 Form Komentar Publik
- Input **nama**, **tanggal** (otomatis terisi), **sumber informasi** (YouTube, Instagram, Google Maps, WhatsApp, Scan di tempat).
- Pilihan penilaian: **Baik, Sedang, Buruk**
- Kolom komentar: *"Berikan alasanmu"*
- Sentimen tidak ditampilkan ke publik.
- Setelah komentar terkirim, pengguna hanya melihat halaman **ucapan terima kasih**.

### 🔒 Dashboard Admin
- Login dengan username & password (`admin` / `123`)
- Visualisasi total komentar per platform.
- Grafik distribusi sentimen berdasarkan penilaian.
- Wordcloud dari seluruh komentar.
- Insight & rekomendasi untuk peningkatan pelayanan.
- Tabel komentar lengkap dengan tombol hapus per baris.
- Download data ke **CSV** dan **TXT**.

---

## 🚀 Cara Menjalankan

1. **Clone repositori / simpan file `app.py`**
2. **Install dependensi**:

```bash
pip install -r requirements.txt