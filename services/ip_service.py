import socket
import subprocess
import urllib.request
from rich.console import Console
from services import firewall_service

console = Console()

def get_local_ip():
    """Mengambil IP lokal sistem."""
    try:
        # Menghubungkan ke IP eksternal (tidak benar-benar mengirim data) untuk mendapatkan interface yang aktif
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "Gagal mendeteksi IP Lokal"

def get_public_ip():
    """Mengambil IP publik sistem menggunakan API eksternal."""
    try:
        with urllib.request.urlopen("https://api.ipify.org", timeout=5) as response:
            return response.read().decode('utf-8')
    except Exception:
        return "Gagal mendeteksi IP Publik (Cek koneksi internet)"

def allow_ip(ip, firewall_type):
    """Mengizinkan IP tertentu pada rantai INPUT, OUTPUT, dan FORWARD."""
    try:
        if firewall_type == "UFW":
            console.print(f"[bold yellow]Mengizinkan IP {ip} menggunakan UFW...[/bold yellow]")
            # UFW allow from IP mencakup input
            subprocess.run(["sudo", "ufw", "allow", "from", ip], check=True)
        elif firewall_type == "IPTABLES":
            console.print(f"[bold yellow]Mengizinkan IP {ip} di INPUT, OUTPUT, dan FORWARD (Iptables)...[/bold yellow]")
            # Aturan untuk ketiga rantai
            subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "ACCEPT"], check=True)
            subprocess.run(["sudo", "iptables", "-A", "OUTPUT", "-d", ip, "-j", "ACCEPT"], check=True)
            subprocess.run(["sudo", "iptables", "-A", "FORWARD", "-s", ip, "-j", "ACCEPT"], check=True)
            subprocess.run(["sudo", "iptables", "-A", "FORWARD", "-d", ip, "-j", "ACCEPT"], check=True)
            firewall_service.save_iptables_rules()
        else:
            console.print("[bold red]Tipe firewall tidak didukung.[/bold red]")
            return False
            
        console.print(f"[bold green]Berhasil mengizinkan akses untuk IP {ip}.[/bold green]")
        return True
    except Exception as e:
        console.print(f"[bold red]Gagal mengizinkan IP: {e}[/bold red]")
        return False

def block_ip(ip, firewall_type):
    """Memblokir IP tertentu."""
    try:
        if firewall_type == "UFW":
            console.print(f"[bold yellow]Memblokir IP {ip} menggunakan UFW...[/bold yellow]")
            subprocess.run(["sudo", "ufw", "deny", "from", ip], check=True)
        elif firewall_type == "IPTABLES":
            console.print(f"[bold yellow]Memblokir IP {ip} menggunakan Iptables...[/bold yellow]")
            subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"], check=True)
            firewall_service.save_iptables_rules()
        else:
            console.print("[bold red]Tipe firewall tidak didukung.[/bold red]")
            return False
            
        console.print(f"[bold green]Berhasil memblokir IP {ip}.[/bold green]")
        return True
    except Exception as e:
        console.print(f"[bold red]Gagal memblokir IP: {e}[/bold red]")
        return False
