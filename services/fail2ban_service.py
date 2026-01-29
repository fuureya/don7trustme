import subprocess
import os
from rich.console import Console
from rich.panel import Panel
from services import ip_service

console = Console()

def is_fail2ban_installed():
    """Mengecek apakah fail2ban terinstall."""
    try:
        result = subprocess.run(["which", "fail2ban-client"], capture_output=True, text=True)
        return result.returncode == 0
    except Exception:
        return False

def install_fail2ban():
    """Menginstall fail2ban (khusus Debian/Ubuntu)."""
    try:
        console.print("[bold yellow]Sedang menginstal Fail2Ban...[/bold yellow]")
        subprocess.run(["sudo", "apt", "update"], check=True)
        subprocess.run(["sudo", "apt", "install", "-y", "fail2ban"], check=True)
        console.print("[bold green]Fail2Ban berhasil diinstal![/bold green]")
        return True
    except Exception as e:
        console.print(f"[bold red]Gagal menginstal Fail2Ban: {e}[/bold red]")
        return False

def setup_fail2ban_ssh(max_retry=5, ban_time="1h", ignore_ip=None):
    """Mengonfigurasi Fail2Ban untuk proteksi SSH."""
    jail_local_path = "/etc/fail2ban/jail.local"
    
    # Ambil IP lokal untuk di-ignore secara default
    my_ip = ip_service.get_local_ip()
    ips_to_ignore = f"127.0.0.1/8 ::1 {my_ip}"
    if ignore_ip:
        ips_to_ignore += f" {ignore_ip}"

    config_content = f"""[DEFAULT]
ignoreip = {ips_to_ignore}
bantime = {ban_time}
findtime = 10m
maxretry = {max_retry}

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
backend = systemd
maxretry = {max_retry}
"""

    try:
        console.print("[bold yellow]Mengonfigurasi /etc/fail2ban/jail.local...[/bold yellow]")
        # Gunakan sudo tee untuk menulis file sistem
        process = subprocess.Popen(["sudo", "tee", jail_local_path], stdin=subprocess.PIPE, text=True)
        process.communicate(input=config_content)
        
        if process.returncode == 0:
            console.print("[bold green]Konfigurasi berhasil ditulis![/bold green]")
            console.print("[bold yellow]Me-restart layanan Fail2Ban...[/bold yellow]")
            subprocess.run(["sudo", "systemctl", "restart", "fail2ban"], check=True)
            subprocess.run(["sudo", "systemctl", "enable", "fail2ban"], check=True)
            console.print("[bold green]Fail2Ban aktif dan berjalan dengan konfigurasi baru.[/bold green]")
            
            # Tampilkan ringkasan status
            console.print(Panel(
                "✅ [bold green]SSH jail aktif[/bold green]\n"
                f"✅ [bold green]Retry limit: {max_retry}[/bold green]\n"
                f"✅ [bold green]Ban time: {ban_time}[/bold green]\n"
                f"✅ [bold green]Ignore IP: {ips_to_ignore}[/bold green]\n"
                "✅ [bold green]Backend log: systemd[/bold green]",
                title="Status Fail2Ban",
                border_style="green"
            ))
            return True
        return False
    except Exception as e:
        console.print(f"[bold red]Gagal mengonfigurasi Fail2Ban: {e}[/bold red]")
        return False

def get_fail2ban_status():
    """Mendapatkan status jail SSH."""
    try:
        result = subprocess.run(["sudo", "fail2ban-client", "status", "sshd"], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        return "Fail2Ban tidak berjalan atau jail sshd tidak aktif."
    except Exception:
        return "Error mengambil status Fail2Ban."
