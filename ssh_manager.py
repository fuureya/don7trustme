import os
import subprocess
from rich.console import Console

console = Console()

def restart_ssh():
    """Me-restart layanan SSH untuk menerapkan perubahan."""
    try:
        subprocess.run(["sudo", "systemctl", "restart", "ssh"], check=True)
        console.print("[bold green]Layanan SSH berhasil di-restart.[/bold green]")
        return True
    except subprocess.CalledProcessError:
        try:
            subprocess.run(["sudo", "service", "ssh", "restart"], check=True)
            console.print("[bold green]Layanan SSH berhasil di-restart.[/bold green]")
            return True
        except subprocess.CalledProcessError:
            console.print("[bold red]Gagal me-restart layanan SSH. Pastikan Anda memiliki hak akses sudo.[/bold red]")
            return False

def disable_root_login():
    """Menonaktifkan login root di SSH."""
    config_path = "/etc/ssh/sshd_config"
    try:
        # Membaca file konfigurasi
        with open(config_path, 'r') as file:
            lines = file.readlines()

        # Mencari dan mengubah PermitRootLogin
        new_lines = []
        found = False
        for line in lines:
            if line.strip().startswith("PermitRootLogin"):
                new_lines.append("PermitRootLogin no\n")
                found = True
            else:
                new_lines.append(line)
        
        if not found:
            new_lines.append("\nPermitRootLogin no\n")

        # Menulis kembali ke file sementara lalu pindahkan dengan sudo
        temp_file = "/tmp/sshd_config_tmp"
        with open(temp_file, 'w') as file:
            file.writelines(new_lines)

        subprocess.run(["sudo", "mv", temp_file, config_path], check=True)
        console.print("[bold green]Berhasil menonaktifkan root login di SSH.[/bold green]")
        return restart_ssh()

    except Exception as e:
        console.print(f"[bold red]Terjadi kesalahan: {e}[/bold red]")
        return False

def change_ssh_port(new_port):
    """Mengubah port default SSH."""
    config_path = "/etc/ssh/sshd_config"
    try:
        # Membaca file konfigurasi
        with open(config_path, 'r') as file:
            lines = file.readlines()

        # Mencari dan mengubah Port
        new_lines = []
        found = False
        for line in lines:
            if line.strip().startswith("Port ") or line.strip() == "Port":
                new_lines.append(f"Port {new_port}\n")
                found = True
            else:
                new_lines.append(line)
        
        if not found:
            new_lines.append(f"\nPort {new_port}\n")

        # Menulis kembali ke file sementara lalu pindahkan dengan sudo
        temp_file = "/tmp/sshd_config_tmp"
        with open(temp_file, 'w') as file:
            file.writelines(new_lines)

        subprocess.run(["sudo", "mv", temp_file, config_path], check=True)
        console.print(f"[bold green]Berhasil mengubah port SSH ke {new_port}.[/bold green]")
        return restart_ssh()

    except Exception as e:
        console.print(f"[bold red]Terjadi kesalahan: {e}[/bold red]")
        return False
