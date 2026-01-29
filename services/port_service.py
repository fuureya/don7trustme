import subprocess
from rich.console import Console
from rich.table import Table

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

def close_port(port):
    """Menutup akses port menggunakan UFW."""
    try:
        # Mencoba menggunakan UFW (Uncomplicated Firewall) yang umum di Linux
        console.print(f"[bold yellow]Mencoba menutup port {port} menggunakan UFW...[/bold yellow]")
        subprocess.run(["sudo", "ufw", "deny", port], check=True)
        console.print(f"[bold green]Berhasil menutup akses ke port {port} melalui UFW.[/bold green]")
        return True
    except subprocess.CalledProcessError:
        # Jika UFW gagal, coba iptables sebagai alternatif
        try:
            console.print(f"[bold yellow]UFW gagal, mencoba menggunakan iptables untuk memblokir port {port}...[/bold yellow]")
            subprocess.run(["sudo", "iptables", "-A", "INPUT", "-p", "tcp", "--destination-port", port, "-j", "DROP"], check=True)
            console.print(f"[bold green]Berhasil memblokir port {port} melalui iptables.[/bold green]")
            return True
        except subprocess.CalledProcessError:
            console.print(f"[bold red]Gagal menutup port. Pastikan Anda memiliki hak akses sudo dan memiliki UFW atau iptables terinstall.[/bold red]")
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
