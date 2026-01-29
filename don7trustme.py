import os
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from skull import SKULL
from services import ssh_service, port_service, firewall_service, ip_service, fail2ban_service, user_service, audit_service, scanner_service

console = Console()

# Global state
scanned_ports_cache = []
firewall_type = "UNKNOWN"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def header():
    console.print(SKULL, style="bold red")
    console.print(
        Align.left(
            Panel(
                "[bold yellow]Don7trustme Firewall Tools[/bold yellow]",
                width=50
            )
        )
    )
    console.print()


def pause():
    console.input("[bold yellow]Tekan Enter untuk melanjutkan...[/bold yellow]")


def kelola_ssh():
    while True:
        clear_screen()
        header()

        console.print(
            Panel(
                f"[bold green]SSH Hardening[/bold green] (Firewall: {firewall_type})\n\n"
                "[cyan]1.[/cyan] Matikan Root Login\n"
                "[cyan]2.[/cyan] Ganti Port SSH\n"
                "[cyan]3.[/cyan] Kembali",
                width=50
            )
        )

        choice = console.input("[bold magenta]Pilih (1/2/3): [/bold magenta]")

        if choice == "1":
            confirm = console.input("[bold yellow]Apakah Anda yakin ingin mematikan Root Login? (y/n): [/bold yellow]")
            if confirm.lower() == 'y':
                ssh_service.disable_root_login()
            pause()
        elif choice == "2":
            port = console.input("[bold yellow]Masukkan port baru yang Anda inginkan: [/bold yellow]")
            if port.isdigit():
                ssh_service.change_ssh_port(port)
            else:
                console.print("[bold red]Port harus berupa angka![/bold red]")
            pause()
        elif choice == "3":
            break
        else:
            console.print("[bold red]Pilihan tidak valid![/bold red]")
            pause()


def kelola_port():
    global scanned_ports_cache
    while True:
        clear_screen()
        header()

        console.print(
            Panel(
                f"[bold green]Manage Port[/bold green] (Firewall: {firewall_type})\n\n"
                "[cyan]1.[/cyan] Scan Port Aktif\n"
                "[cyan]2.[/cyan] Tutup Port Aktif\n"
                "[cyan]3.[/cyan] Proteksi Scan Nmap\n"
                "[cyan]4.[/cyan] Aktifkan Port\n"
                "[cyan]5.[/cyan] Kembali",
                width=50
            )
        )

        choice = console.input("[bold magenta]Pilih (1/2/3/4/5): [/bold magenta]")

        if choice == "1":
            console.print("[bold blue]Memindai port aktif...[/bold blue]")
            scanned_ports_cache = port_service.get_active_ports()
            port_service.display_ports_table(scanned_ports_cache)
            pause()
        elif choice == "2":
            if not scanned_ports_cache:
                console.print("[bold red]Anda harus melakukan Scan Port Aktif (Opsi 1) terlebih dahulu![/bold red]")
                pause()
                continue
            
            port_service.display_ports_table(scanned_ports_cache)
            idx_input = console.input("[bold magenta]Pilih nomor port yang ingin ditutup (0 untuk batal): [/bold magenta]")
            
            if idx_input.isdigit():
                idx = int(idx_input)
                if idx == 0:
                    continue
                if 1 <= idx <= len(scanned_ports_cache):
                    port_to_close = scanned_ports_cache[idx-1]
                    confirm = console.input(f"[bold yellow]Yakin ingin menutup port {port_to_close}? (y/n): [/bold yellow]")
                    if confirm.lower() == 'y':
                        port_service.close_port(port_to_close, firewall_type)
                        # Refresh cache setelah menutup port
                        console.print("[bold blue]Memperbarui daftar port...[/bold blue]")
                        scanned_ports_cache = port_service.get_active_ports()
                    pause()
                else:
                    console.print("[bold red]Nomor tidak valid![/bold red]")
                    pause()
            else:
                console.print("[bold red]Masukkan angka![/bold red]")
                pause()
        elif choice == "3":
            console.print(Panel(
                "[bold yellow]INFO:[/bold yellow]\n"
                "Proses ini [bold red]tidak 100%[/bold red] menjadi anti scan,\n"
                "tapi memperlambat scan untuk orang mendapatkan informasi server anda.",
                width=50,
                border_style="yellow"
            ))
            confirm = console.input("[bold yellow]Aktifkan proteksi ini? (y/n): [/bold yellow]")
            if confirm.lower() == 'y':
                firewall_service.enable_nmap_protection(firewall_type)
            pause()
        elif choice == "4":
            new_port = console.input("[bold yellow]Masukkan port yang ingin diaktifkan (ketik 'cancel' untuk batal): [/bold yellow]")
            if new_port.lower() == 'cancel':
                console.print("[bold cyan]Proses aktivasi port dibatalkan.[/bold cyan]")
            elif new_port.isdigit():
                port_service.open_port(new_port, firewall_type)
            else:
                console.print("[bold red]Port harus berupa angka atau ketik 'cancel'![/bold red]")
            pause()
        elif choice == "5":
            break
        else:
            console.print("[bold red]Pilihan tidak valid![/bold red]")
            pause()


def kelola_ip():
    while True:
        clear_screen()
        header()

        console.print(
            Panel(
                f"[bold green]Manage IP[/bold green] (Firewall: {firewall_type})\n\n"
                "[cyan]1.[/cyan] Cek IP Lokal\n"
                "[cyan]2.[/cyan] Cek IP Publik\n"
                "[cyan]3.[/cyan] Allow Access IP (IN/OUT/FWD)\n"
                "[cyan]4.[/cyan] Blokir IP\n"
                "[cyan]5.[/cyan] Kembali",
                width=50
            )
        )

        choice = console.input("[bold magenta]Pilih (1/2/3/4/5): [/bold magenta]")

        if choice == "1":
            console.print(f"[bold blue]IP Lokal: {ip_service.get_local_ip()}[/bold blue]")
            pause()
        elif choice == "2":
            console.print("[bold blue]Sedang mengambil IP Publik...[/bold blue]")
            console.print(f"[bold blue]IP Publik: {ip_service.get_public_ip()}[/bold blue]")
            pause()
        elif choice == "3":
            ip = console.input("[bold yellow]Masukkan IP yang ingin diizinkan: [/bold yellow]")
            if ip:
                if ip_service.validate_ip(ip):
                    ip_service.allow_ip(ip, firewall_type)
                else:
                    console.print("[bold red]Format IP tidak sesuai![/bold red]")
            pause()
        elif choice == "4":
            ip = console.input("[bold yellow]Masukkan IP yang ingin diblokir: [/bold yellow]")
            if ip:
                if ip_service.validate_ip(ip):
                    ip_service.block_ip(ip, firewall_type)
                else:
                    console.print("[bold red]Format IP tidak sesuai![/bold red]")
            pause()
        elif choice == "5":
            break
        else:
            console.print("[bold red]Pilihan tidak valid![/bold red]")
            pause()



def setup_fail2ban():
    clear_screen()
    header()
    console.print(Panel("[bold green]Setup Fail2Ban (SSH Anti Brute-force)[/bold green]", width=50))
    
    if not fail2ban_service.is_fail2ban_installed():
        console.print("[bold red]Fail2Ban belum terinstall pada sistem ini.[/bold red]")
        confirm = console.input("[bold yellow]Ingin menginstal Fail2Ban sekarang? (y/n): [/bold yellow]")
        if confirm.lower() == 'y':
            if not fail2ban_service.install_fail2ban():
                pause()
                return
        else:
            return

    console.print("\n[bold cyan]Konfigurasi Jails SSH:[/bold cyan]")
    retry = console.input("[bold yellow]Masukkan Max Retry (default 5): [/bold yellow]") or "5"
    btime = console.input("[bold yellow]Masukkan Ban Time (cth: 1h, 1d, 10m - default 1h): [/bold yellow]") or "1h"
    ignore = console.input("[bold yellow]IP tambahan untuk di-ignore (kosongkan jika tidak ada): [/bold yellow]")
    
    if ignore and not ip_service.validate_ip(ignore):
        console.print("[bold red]Format IP tambahan tidak valid! Mengabaikan IP tambahan.[/bold red]")
        ignore = None

    fail2ban_service.setup_fail2ban_ssh(max_retry=retry, ban_time=btime, ignore_ip=ignore)
    pause()


def kelola_user_access():
    while True:
        clear_screen()
        header()
        console.print(
            Panel(
                "[bold green]User & Access Control[/bold green]\n\n"
                "[cyan]1.[/cyan] Account Locking (pam_faillock)\n"
                "[cyan]2.[/cyan] Restrict /etc/shadow\n"
                "[cyan]3.[/cyan] Kembali",
                width=50
            )
        )
        choice = console.input("[bold magenta]Pilih (1/2/3): [/bold magenta]")

        if choice == "1":
            console.print(Panel(
                "[bold cyan]FITUR: Account Locking (pam_faillock)[/bold cyan]\n"
                "Mengunci akun secara otomatis jika gagal login sebanyak [bold red]5 kali[/bold red].\n"
                "Akun akan dikunci selama [bold red]15 menit[/bold red] (900 detik).\n"
                "Ini mencegah serangan brute-force pada password linux mas.",
                border_style="cyan"
            ))
            confirm = console.input("[bold yellow]Yakin ingin lanjut? (y/n): [/bold yellow]")
            if confirm.lower() == 'y':
                user_service.setup_account_locking()
            pause()
        elif choice == "2":
            console.print(Panel(
                "[bold cyan]FITUR: Restrict /etc/shadow[/bold cyan]\n"
                "Memastikan file /etc/shadow (yang berisi hash password)\n"
                "hanya bisa dibaca oleh user root. Sangat krusial buat keamanan!",
                border_style="cyan"
            ))
            confirm = console.input("[bold yellow]Yakin ingin lanjut? (y/n): [/bold yellow]")
            if confirm.lower() == 'y':
                user_service.restrict_shadow_file()
            pause()
        elif choice == "3":
            break

def kelola_audit_monitoring():
    while True:
        clear_screen()
        header()
        console.print(
            Panel(
                "[bold green]Audit & Monitoring[/bold green]\n\n"
                "[cyan]1.[/cyan] Setup Auditd\n"
                "[cyan]2.[/cyan] Setup Logwatch\n"
                "[cyan]3.[/cyan] Kembali",
                width=50
            )
        )
        choice = console.input("[bold magenta]Pilih (1/2/3): [/bold magenta]")

        if choice == "1":
            console.print(Panel(
                "[bold cyan]FITUR: Auditd Setup[/bold cyan]\n"
                "Mencatat setiap ada perubahan pada file sensitif seperti\n"
                "/etc/passwd atau /etc/ssh/sshd_config secara real-time.",
                border_style="cyan"
            ))
            confirm = console.input("[bold yellow]Yakin ingin lanjut? (y/n): [/bold yellow]")
            if confirm.lower() == 'y':
                audit_service.setup_auditd()
            pause()
        elif choice == "2":
            console.print(Panel(
                "[bold cyan]FITUR: Logwatch Setup[/bold cyan]\n"
                "Membuat rangkuman aktivitas log sistem setiap harinya.\n"
                "Membantu mas memantau aktivitas mencurigakan dengan mudah.",
                border_style="cyan"
            ))
            confirm = console.input("[bold yellow]Yakin ingin lanjut? (y/n): [/bold yellow]")
            if confirm.lower() == 'y':
                audit_service.setup_logwatch()
            pause()
        elif choice == "3":
            break

def kelola_scanners():
    while True:
        clear_screen()
        header()
        console.print(
            Panel(
                "[bold green]Malware & Vulnerability Detection[/bold green]\n\n"
                "[cyan]1.[/cyan] Rootkit Hunter (rkhunter)\n"
                "[cyan]2.[/cyan] Lynis Security Audit\n"
                "[cyan]3.[/cyan] Kembali",
                width=50
            )
        )
        choice = console.input("[bold magenta]Pilih (1/2/3): [/bold magenta]")

        if choice == "1":
            console.print(Panel(
                "[bold cyan]FITUR: Rootkit Hunter[/bold cyan]\n"
                "Scan sistem untuk mendeteksi rootkits, backdoors,\n"
                "dan eksploitasi lokal lainnya yang berbahaya.",
                border_style="cyan"
            ))
            confirm = console.input("[bold yellow]Yakin ingin lanjut? (y/n): [/bold yellow]")
            if confirm.lower() == 'y':
                scanner_service.setup_rkhunter()
            pause()
        elif choice == "2":
            console.print(Panel(
                "[bold cyan]FITUR: Lynis Integration[/bold cyan]\n"
                "Melakukan audit keamanan sistem secara mendalam dan\n"
                "menampilkan 'Hardening Index' (Skor Keamanan) server mas.",
                border_style="cyan"
            ))
            confirm = console.input("[bold yellow]Yakin ingin lanjut? (y/n): [/bold yellow]")
            if confirm.lower() == 'y':
                scanner_service.run_lynis_scan()
            pause()
        elif choice == "3":
            break


def main():
    global firewall_type
    
    # Firewall Analysis System State pada Startup
    clear_screen()
    header()
    console.print(Panel("[bold cyan]Menjalankan Analisis Sistem...[/bold cyan]", width=50))
    firewall_type = firewall_service.detect_firewall()
    console.print(firewall_service.get_firewall_status_message(firewall_type))
    
    if firewall_type == "IPTABLES":
        if not firewall_service.check_iptables_persistent():
            console.print()
            console.print(Panel(
                "[bold red]PERINGATAN:[/bold red]\n"
                "Package [bold yellow]iptables-persistent[/bold yellow] tidak terdeteksi.\n"
                "Silakan install dlu package yang di perlukan:\n"
                "[cyan]sudo apt install iptables-persistent[/cyan]\n"
                "agar aturan firewall bersifat [bold green]PERMANEN[/bold green] setelah reboot.",
                border_style="red",
                width=52
            ))
    
    console.print()
    pause()

    while True:
        clear_screen()
        header()

        console.print(
            Panel(
                "[bold green]Menu Utama[/bold green]\n\n"
                "[cyan]1.[/cyan] SSH Hardening\n"
                "[cyan]2.[/cyan] Manage Port\n"
                "[cyan]3.[/cyan] Manage IP\n"
                "[cyan]4.[/cyan] Setup Fail2Ban\n"
                "[cyan]5.[/cyan] User Access Control\n"
                "[cyan]6.[/cyan] Audit & Monitoring\n"
                "[cyan]7.[/cyan] Scanners (Malware/Audit)\n"
                "[cyan]8.[/cyan] Keluar",
                width=50
            )
        )

        choice = console.input("[bold magenta]Masukkan pilihan (1-8): [/bold magenta]")

        if choice == "1":
            kelola_ssh()
        elif choice == "2":
            kelola_port()
        elif choice == "3":
            kelola_ip()
        elif choice == "4":
            setup_fail2ban()
        elif choice == "5":
            kelola_user_access()
        elif choice == "6":
            kelola_audit_monitoring()
        elif choice == "7":
            kelola_scanners()
        elif choice == "8":
            console.print(
                Panel(
                    "[bold red]Terima kasih telah menggunakan Don7trustme Tools[/bold red]",
                    width=50
                )
            )
            break
        else:
            console.print("[bold red]Pilihan tidak valid![/bold red]")
            pause()


if __name__ == "__main__":
    main()
