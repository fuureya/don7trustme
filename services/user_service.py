import subprocess
import os
from rich.console import Console

console = Console()

def restrict_shadow_file():
    """Membatasi akses file /etc/shadow hanya untuk root."""
    try:
        console.print("[bold yellow]Membatasi akses /etc/shadow...[/bold yellow]")
        subprocess.run(["sudo", "chown", "root:root", "/etc/shadow"], check=True)
        subprocess.run(["sudo", "chmod", "600", "/etc/shadow"], check=True)
        console.print("[bold green]Berhasil! File /etc/shadow sekarang hanya bisa dibaca oleh root.[/bold green]")
        return True
    except Exception as e:
        console.print(f"[bold red]Gagal membatasi akses file shadow: {e}[/bold red]")
        return False

def setup_account_locking(deny_count=5, unlock_time=900):
    """Mengonfigurasi pam_faillock untuk mengunci akun setelah kegagalan login."""
    try:
        console.print("[bold yellow]Mengonfigurasi penguncian akun (pam_faillock)...[/bold yellow]")
        
        # Cek apakah faillock didukung (biasanya ada di /etc/pam.d/common-auth)
        pam_auth_path = "/etc/pam.d/common-auth"
        if not os.path.exists(pam_auth_path):
            console.print("[bold red]File konfigurasi PAM tidak ditemukan.[/bold red]")
            return False

        # Baca isi file
        with open(pam_auth_path, 'r') as f:
            lines = f.readlines()

        # Sangat hati-hati dalam mengedit file PAM. Kita akan menambahkan baris faillock
        # jika belum ada. Ini adalah operasi yang berisiko jika salah.
        faillock_preauth = f"auth    required    pam_faillock.so preauth silent audit deny={deny_count} unlock_time={unlock_time}\n"
        faillock_authfail = f"auth    [default=die]    pam_faillock.so authfail audit deny={deny_count} unlock_time={unlock_time}\n"
        faillock_authsucc = "auth    sufficient    pam_faillock.so authsucc audit deny={deny_count} unlock_time={unlock_time}\n"

        # Cek apakah sudah ada faillock
        if any("pam_faillock.so" in line for line in lines):
            console.print("[bold blue]Konfigurasi faillock sudah ditemukan. Melewati langkah ini untuk menghindari duplikasi.[/bold blue]")
            return True

        # Kita tambahkan di bagian atas file untuk preauth
        new_lines = [faillock_preauth]
        for line in lines:
            new_lines.append(line)
        
        # Tambahkan authfail dan authsucc di tempat yang sesuai (biasanya setelah pam_unix.so)
        # Untuk keamanan tool ini, kita akan menggunakan perintah sed yang lebih standar
        # agar tidak merusak file jika scripting python gagal di tengah jalan.
        
        # Menggunakan shell commands untuk injeksi yang lebih aman pada file kritis
        cmd = (
            f"sudo sed -i '1i auth    required    pam_faillock.so preauth silent audit deny={deny_count} unlock_time={unlock_time}' {pam_auth_path} && "
            f"sudo sed -i '/pam_unix.so/a auth    [default=die]    pam_faillock.so authfail audit deny={deny_count} unlock_time={unlock_time}' {pam_auth_path} && "
            f"sudo sed -i '/pam_faillock.so authfail/a auth    sufficient    pam_faillock.so authsucc audit deny={deny_count} unlock_time={unlock_time}' {pam_auth_path}"
        )
        
        subprocess.run(cmd, shell=True, check=True)
        
        console.print(f"[bold green]Berhasil! Akun akan dikunci setelah {deny_count} kali gagal login selama {unlock_time} detik.[/bold green]")
        return True
    except Exception as e:
        console.print(f"[bold red]Gagal mengonfigurasi penguncian akun: {e}[/bold red]")
        return False
