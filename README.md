# Don7trustme Tools

A simple, interactive command-line interface (CLI) tool in Python designed to help manage `iptables` rules for ports and IP addresses. This tool provides a user-friendly menu to simplify common `iptables` operations.

## Setup Proyek

Ikuti langkah-langkah di bawah ini untuk mengatur dan menjalankan proyek ini di lingkungan lokal Anda.

### 1. Klon Repositori (Opsional, jika ini bagian dari repositori)

Jika proyek ini adalah bagian dari repositori Git, Anda bisa mengklonnya:
```bash
# Contoh: git clone <URL_REPOSITORI>
# cd <nama_folder_repositori>
```
Jika tidak, pastikan Anda berada di direktori yang sama dengan file `don7trustme.py` dan `requirements.txt`.

### 2. Buat dan Aktifkan Virtual Environment

Sangat disarankan untuk menggunakan *virtual environment* untuk mengelola dependensi proyek Anda secara terpisah.

```bash
# Buat virtual environment
python3 -m venv venv

# Aktifkan virtual environment
# Di Linux/macOS:
source venv/bin/activate

# Di Windows (Command Prompt):
venv\Scripts\activate.bat

# Di Windows (PowerShell):
venv\Scripts\Activate.ps1
```

Anda akan melihat `(venv)` di awal *prompt* terminal Anda, menandakan bahwa *virtual environment* sudah aktif.

### 3. Instal Dependensi

Setelah *virtual environment* aktif, instal semua dependensi yang diperlukan menggunakan `pip`:

```bash
pip install -r requirements.txt
```

### 4. Jalankan Aplikasi

Setelah semua dependensi terinstal, Anda bisa menjalankan *Don7trustme Tools*:

```bash
python don7trustme.py
```

### 5. Penggunaan

Setelah aplikasi berjalan, Anda akan disambut dengan tampilan `Don7trustme Tools` dan pilihan menu:

1.  **Kelola Port**: Fungsionalitas untuk mengatur aturan `iptables` terkait port.
2.  **Kelola IP**: Fungsionalitas untuk mengatur aturan `iptables` terkait alamat IP.
3.  **Keluar**: Untuk menutup aplikasi.

Pilih opsi yang diinginkan dengan memasukkan angka dan tekan Enter.
