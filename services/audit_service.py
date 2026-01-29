import subprocess
import os
from rich.console import Console

console = Console()

def setup_auditd():
    """Menginstal dan mengonfigurasi Auditd untuk memantau file sensitif."""
    try:
        console.print("[bold yellow]Sedang mengecek/menginstal Auditd...[/bold yellow]")
        subprocess.run(["sudo", "apt", "update"], check=True)
        subprocess.run(["sudo", "apt", "install", "-y", "auditd"], check=True)
        
        rules_path = "/etc/audit/rules.d/audit.rules"
        rules_content = """
# Pantau perubahan pada file password
-w /etc/passwd -p wa -k identity
-w /etc/group -p wa -k identity
-w /etc/shadow -p wa -k identity

# Pantau perubahan pada konfigurasi SSH
-w /etc/ssh/sshd_config -p wa -k sshd_config
"""
        
        console.print("[bold yellow]Menambahkan aturan audit...[/bold yellow]")
        process = subprocess.Popen(["sudo", "tee", "-a", rules_path], stdin=subprocess.PIPE, text=True)
        process.communicate(input=rules_content)
        
        subprocess.run(["sudo", "service", "auditd", "restart"], check=True)
        console.print("[bold green]Auditd berhasil dikonfigurasi dan dijalankan.[/bold green]")
        return True
    except Exception as e:
        console.print(f"[bold red]Gagal mengonfigurasi Auditd: {e}[/bold red]")
        return False

def setup_logwatch():
    """Menginstal Logwatch untuk ringkasan aktivitas log harian."""
    try:
        console.print("[bold yellow]Menginstal Logwatch...[/bold yellow]")
        subprocess.run(["sudo", "apt", "update"], check=True)
        subprocess.run(["sudo", "apt", "install", "-y", "logwatch"], check=True)
        
        # Logwatch biasanya berjalan harian via cron. Kita cukup pastikan terinstal.
        console.print("[bold green]Logwatch berhasil diinstal. Anda akan menerima ringkasan log harian di sistem.[/bold green]")
        return True
    except Exception as e:
        console.print(f"[bold red]Gagal menginstal Logwatch: {e}[/bold red]")
        return False

def is_auditd_installed():
    """Mengecek apakah auditd terinstall."""
    return os.path.exists("/usr/sbin/auditd")

def is_logwatch_installed():
    """Mengecek apakah logwatch terinstall."""
    return os.path.exists("/usr/sbin/logwatch")

def get_audit_logs(limit=10):
    """Membaca log audit terbaru menggunakan ausearch."""
    try:
        # Mencari event audit terbaru
        result = subprocess.run(["sudo", "ausearch", "-m", "CONFIG_CHANGE", "-i", "--start", "today"], capture_output=True, text=True)
        if result.returncode == 0 and result.stdout:
            return result.stdout
        return "Belum ada log audit perubahan konfigurasi untuk hari ini."
    except Exception as e:
        return f"Gagal membaca log audit: {e}"

def get_logwatch_report():
    """Menghasilkan report logwatch instan untuk hari ini."""
    try:
        console.print("[bold yellow]Sedang mengolah data log (mungkin butuh waktu)...[/bold yellow]")
        result = subprocess.run(["sudo", "logwatch", "--detail", "low", "--range", "today", "--output", "stdout"], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        return "Gagal menghasilkan report Logwatch."
    except Exception as e:
        return f"Error: {e}"
