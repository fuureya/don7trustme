import subprocess
from rich.console import Console
from rich.table import Table
from services import firewall_service

console = Console()

def get_active_ports():
    """Memindai port TCP yang sedang listening di sistem."""
    try:
        # Menjalankan perintah ss -tuln untuk mendapatkan port listening
        result = subprocess.run(["ss", "-tuln"], capture_output=True, text=True, check=True)
        lines = result.stdout.strip().split('\n')
        
        active_ports = []
        for line in lines[1:]:  # Skip header
            parts = line.split()
            if len(parts) >= 5:
                address = parts[4]
                # Format address biasanya 0.0.0.0:80 atau [::]:80 atau *:80
                port = address.split(':')[-1]
                if port.isdigit() and port not in active_ports:
                    active_ports.append(port)
        
        # Urutkan port secara numerik
        active_ports.sort(key=int)
        return active_ports
    except Exception as e:
        console.print(f"[bold red]Gagal memindai port: {e}[/bold red]")
        return []

def close_port(port, firewall_type):
    """Menutup akses port menggunakan firewall yang terdeteksi."""
    try:
        if firewall_type == "UFW":
            console.print(f"[bold yellow]Menutup port {port} menggunakan UFW...[/bold yellow]")
            subprocess.run(["sudo", "ufw", "deny", port], check=True)
        elif firewall_type == "IPTABLES":
            console.print(f"[bold yellow]Menutup port {port} menggunakan Iptables...[/bold yellow]")
            subprocess.run(["sudo", "iptables", "-A", "INPUT", "-p", "tcp", "--destination-port", port, "-j", "DROP"], check=True)
            firewall_service.save_iptables_rules()
        else:
            console.print("[bold red]Tipe firewall tidak didukung or tidak terdeteksi.[/bold red]")
            return False
            
        console.print(f"[bold green]Berhasil menutup akses ke port {port}.[/bold green]")
        return True
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Gagal menutup port: {e}[/bold red]")
        return False
    except Exception as e:
        console.print(f"[bold red]Terjadi kesalahan: {e}[/bold red]")
        return False

def open_port(port, firewall_type):
    """Membuka akses port menggunakan firewall yang terdeteksi."""
    try:
        if firewall_type == "UFW":
            console.print(f"[bold yellow]Membuka port {port} menggunakan UFW...[/bold yellow]")
            subprocess.run(["sudo", "ufw", "allow", port], check=True)
        elif firewall_type == "IPTABLES":
            console.print(f"[bold yellow]Membuka port {port} menggunakan Iptables...[/bold yellow]")
            subprocess.run(["sudo", "iptables", "-A", "INPUT", "-p", "tcp", "--destination-port", port, "-j", "ACCEPT"], check=True)
            firewall_service.save_iptables_rules()
        else:
            console.print("[bold red]Tipe firewall tidak didukung or tidak terdeteksi.[/bold red]")
            return False
            
        console.print(f"[bold green]Berhasil membuka akses ke port {port}.[/bold green]")
        return True
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Gagal membuka port: {e}[/bold red]")
        return False
    except Exception as e:
        console.print(f"[bold red]Terjadi kesalahan: {e}[/bold red]")
        return False

def display_ports_table(ports):
    """Menampilkan daftar port dalam bentuk tabel yang bagus."""
    if not ports:
        console.print("[bold yellow]Tidak ada port aktif yang ditemukan.[/bold yellow]")
        return

    table = Table(title="Port Aktif (LISTENING)")
    table.add_column("No", justify="right", style="cyan", no_wrap=True)
    table.add_column("Port", style="magenta")
    
    for idx, port in enumerate(ports, 1):
        table.add_row(str(idx), port)
    
    console.print(table)
