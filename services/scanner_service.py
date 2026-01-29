import subprocess
import os
from rich.console import Console

console = Console()

def setup_rkhunter():
    """Menginstal dan menjalankan scan awal Rkhunter."""
    try:
        console.print("[bold yellow]Menginstal Rkhunter...[/bold yellow]")
        subprocess.run(["sudo", "apt", "update"], check=True)
        subprocess.run(["sudo", "apt", "install", "-y", "rkhunter"], check=True)
        
        console.print("[bold yellow]Memperbarui database rkhunter...[/bold yellow]")
        subprocess.run(["sudo", "rkhunter", "--update"], check=True)
        subprocess.run(["sudo", "rkhunter", "--propupd"], check=True)
        
        console.print("[bold green]Rkhunter berhasil disiapkan.[/bold green]")
        return True
    except Exception as e:
        console.print(f"[bold red]Gagal menyiapkan Rkhunter: {e}[/bold red]")
        return False

def run_lynis_scan():
    """Menginstal Lynis dan menjalankan audit dasar."""
    try:
        if not is_lynis_installed():
            console.print("[bold yellow]Menginstal Lynis...[/bold yellow]")
            subprocess.run(["sudo", "apt", "update"], check=True)
            subprocess.run(["sudo", "apt", "install", "-y", "lynis"], check=True)
        
        console.print("[bold yellow]Menjalankan audit sistem dengan Lynis (Quick Scan)...[/bold yellow]")
        # Menjalankan audit sistem dan mencari Hardening Index
        result = subprocess.run(["sudo", "lynis", "audit", "system", "--quick"], capture_output=True, text=True)
        
        # Tampilkan beberapa baris terakhir yang biasanya berisi skor
        output = result.stdout
        for line in output.split("\n"):
            if "Hardening index" in line:
                console.print(f"[bold green]{line.strip()}[/bold green]")
        
        console.print("[bold cyan]Laporan lengkap Lynis dapat ditemukan di /var/log/lynis.log[/bold cyan]")
        return True
    except Exception as e:
        console.print(f"[bold red]Gagal menjalankan Lynis: {e}[/bold red]")
        return False

def is_rkhunter_installed():
    """Mengecek apakah rkhunter terinstall."""
    return os.path.exists("/usr/bin/rkhunter")

def is_lynis_installed():
    """Mengecek apakah lynis terinstall."""
    return os.path.exists("/usr/bin/lynis") or os.path.exists("/usr/sbin/lynis")

def get_rkhunter_log():
    """Membaca log rkhunter terbaru."""
    log_path = "/var/log/rkhunter.log"
    try:
        if os.path.exists(log_path):
            # Ambil ringkasan di akhir log
            result = subprocess.run(["sudo", "tail", "-n", "30", log_path], capture_output=True, text=True)
            return result.stdout
        return "File log rkhunter tidak ditemukan. Pastikan sudah pernah menjalankan scan."
    except Exception as e:
        return f"Gagal membaca log: {e}"

def get_lynis_report():
    """Membaca ringkasan laporan lynis terbaru."""
    log_path = "/var/log/lynis-report.dat"
    try:
        if os.path.exists(log_path):
            result = subprocess.run(["sudo", "grep", "-E", "hardening_index|tests_executed", log_path], capture_output=True, text=True)
            return result.stdout
        return "File laporan lynis tidak ditemukan. Silakan jalankan audit sistem terlebih dahulu."
    except Exception as e:
        return f"Gagal membaca laporan: {e}"
