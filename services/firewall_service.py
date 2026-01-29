import subprocess
from rich.console import Console

console = Console()

def detect_firewall():
    """Mendeteksi apakah sistem menggunakan UFW atau Iptables."""
    try:
        # Cek apakah UFW terinstall dan aktif
        ufw_check = subprocess.run(["sudo", "ufw", "status"], capture_output=True, text=True)
        if ufw_check.returncode == 0 and "Status: active" in ufw_check.stdout:
            return "UFW"
        
        # Jika UFW tidak aktif, cek iptables
        iptables_check = subprocess.run(["sudo", "iptables", "-L"], capture_output=True, text=True)
        if iptables_check.returncode == 0:
            return "IPTABLES"
            
    except Exception:
        pass
    
    return "UNKNOWN"

def check_iptables_persistent():
    """Mengecek apakah iptables-persistent terinstall."""
    # Cek keberadaan file konfigurasi atau perintah netfilter-persistent
    try:
        check = subprocess.run(["which", "netfilter-persistent"], capture_output=True, text=True)
        return check.returncode == 0
    except Exception:
        return False

def save_iptables_rules():
    """Menyimpan aturan iptables menggunakan netfilter-persistent."""
    try:
        console.print("[bold yellow]Menyimpan aturan Iptables agar permanen...[/bold yellow]")
        subprocess.run(["sudo", "netfilter-persistent", "save"], check=True)
        console.print("[bold green]Aturan Iptables berhasil disimpan.[/bold green]")
        return True
    except Exception as e:
        console.print(f"[bold red]Gagal menyimpan aturan Iptables: {e}[/bold red]")
        return False

def get_firewall_status_message(firewall_type):
    if firewall_type == "UFW":
        return "[bold green]Sistem mendeteksi penggunaan UFW (Uncomplicated Firewall).[/bold green]"
    elif firewall_type == "IPTABLES":
        return "[bold yellow]Sistem mendeteksi penggunaan Iptables secara langsung.[/bold yellow]"
    else:
        return "[bold red]Sistem tidak mendeteksi firewall (UFW/Iptables) yang aktif.[/bold red]"
