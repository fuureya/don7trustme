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
        if not os.path.exists("/usr/bin/lynis") and not os.path.exists("/usr/sbin/lynis"):
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
