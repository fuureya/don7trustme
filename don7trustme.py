import os
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from skull import SKULL
import ssh_manager

console = Console()


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
                "[bold green]SSH Hardening[/bold green]\n\n"
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
                ssh_manager.disable_root_login()
            pause()
        elif choice == "2":
            port = console.input("[bold yellow]Masukkan port baru yang Anda inginkan: [/bold yellow]")
            if port.isdigit():
                ssh_manager.change_ssh_port(port)
            else:
                console.print("[bold red]Port harus berupa angka![/bold red]")
            pause()
        elif choice == "3":
            break
        else:
            console.print("[bold red]Pilihan tidak valid![/bold red]")
            pause()


def kelola_port():
    while True:
        clear_screen()
        header()

        console.print(
            Panel(
                "[bold green]Manage Port[/bold green]\n\n"
                "[cyan]1.[/cyan] Scan Port\n"
                "[cyan]2.[/cyan] Buka Port (dummy)\n"
                "[cyan]3.[/cyan] Kembali",
                width=50
            )
        )

        choice = console.input("[bold magenta]Pilih (1/2/3): [/bold magenta]")

        if choice == "1":
            console.print("[bold blue]Fitur scan port belum diimplementasikan.[/bold blue]")
            pause()
        elif choice == "2":
            console.print("[bold blue]Fitur buka port belum diimplementasikan.[/bold blue]")
            pause()
        elif choice == "3":
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
                "[bold green]Manage IP[/bold green]\n\n"
                "[cyan]1.[/cyan] Cek IP Lokal\n"
                "[cyan]2.[/cyan] Cek IP Publik\n"
                "[cyan]3.[/cyan] Kembali",
                width=50
            )
        )

        choice = console.input("[bold magenta]Pilih (1/2/3): [/bold magenta]")

        if choice == "1":
            console.print("[bold blue]IP Lokal: 127.0.0.1 (dummy)[/bold blue]")
            pause()
        elif choice == "2":
            console.print("[bold blue]IP Publik: 0.0.0.0 (dummy)[/bold blue]")
            pause()
        elif choice == "3":
            break
        else:
            console.print("[bold red]Pilihan tidak valid![/bold red]")
            pause()


def main():
    while True:
        clear_screen()
        header()

        console.print(
            Panel(
                "[bold green]Menu Utama[/bold green]\n\n"
                "[cyan]1.[/cyan] SSH Hardening\n"
                "[cyan]2.[/cyan] Manage Port\n"
                "[cyan]3.[/cyan] Manage IP\n"
                "[cyan]4.[/cyan] Keluar",
                width=50
            )
        )

        choice = console.input("[bold magenta]Masukkan pilihan (1/2/3/4): [/bold magenta]")

        if choice == "1":
            kelola_ssh()
        elif choice == "2":
            kelola_port()
        elif choice == "3":
            kelola_ip()
        elif choice == "4":
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
