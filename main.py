#!/usr/bin/env python3
"""
Penetration Testing Toolkit - Main Module
A toolkit for network scanning and brute force attacks
"""

import os
import sys
import argparse
from colorama import Fore, Style, init

# Add the parent directory to sys.path to allow importing modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our modules
from scanner.port_scanner import PortScanner
from brute_force.ssh_brute_force import SSHBruteForce

# Initialize colorama
init(autoreset=True)

def print_banner():
    """Print the toolkit banner"""
    banner = f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║  {Fore.RED}██████╗ ███████╗███╗   ██╗████████╗███████╗███████╗████████╗{Fore.CYAN}  ║
║  {Fore.RED}██╔══██╗██╔════╝████╗  ██║╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝{Fore.CYAN}  ║
║  {Fore.RED}██████╔╝█████╗  ██╔██╗ ██║   ██║   █████╗  ███████╗   ██║   {Fore.CYAN}  ║
║  {Fore.RED}██╔═══╝ ██╔══╝  ██║╚██╗██║   ██║   ██╔══╝  ╚════██║   ██║   {Fore.CYAN}  ║
║  {Fore.RED}██║     ███████╗██║ ╚████║   ██║   ███████╗███████║   ██║   {Fore.CYAN}  ║
║  {Fore.RED}╚═╝     ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚══════╝   ╚═╝   {Fore.CYAN}  ║
║                                                               ║
║  {Fore.GREEN}Penetration Testing Toolkit{Fore.CYAN}                               ║
║  {Fore.YELLOW}Network Scanning & Brute Force Tool{Fore.CYAN}                       ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
    """
    print(banner)

def setup_argparse():
    """Set up command line argument parsing"""
    parser = argparse.ArgumentParser(description="Penetration Testing Toolkit")

    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # GUI command
    gui_parser = subparsers.add_parser("gui", help="Launch the graphical user interface")

    # Scan command
    scan_parser = subparsers.add_parser("scan", help="Perform network scanning")
    scan_parser.add_argument("target", help="Target IP address or hostname")
    scan_parser.add_argument("--ports", "-p", default="1-1000", help="Port range to scan (default: 1-1000)")
    scan_parser.add_argument("--type", "-t", choices=["basic", "comprehensive", "stealth"], default="basic",
                            help="Type of scan to perform (default: basic)")

    # Brute force command
    brute_parser = subparsers.add_parser("brute", help="Perform brute force attacks")
    brute_parser.add_argument("target", help="Target IP address or hostname")
    brute_parser.add_argument("--service", "-s", choices=["ssh"], default="ssh",
                             help="Service to brute force (default: ssh)")
    brute_parser.add_argument("--username", "-u", help="Username for single user brute force")
    brute_parser.add_argument("--password-list", "-P", help="Path to password list file")
    brute_parser.add_argument("--usernames-list", "-U", help="Path to usernames list file")
    brute_parser.add_argument("--credentials-list", "-C", help="Path to credentials list file (username:password format)")

    return parser

def handle_scan_command(args):
    """Handle the scan command"""
    scanner = PortScanner()

    if args.type == "basic":
        scanner.basic_scan(args.target, args.ports)
    elif args.type == "comprehensive":
        scanner.comprehensive_scan(args.target, args.ports)
    elif args.type == "stealth":
        scanner.stealth_scan(args.target, args.ports)

def handle_brute_command(args):
    """Handle the brute force command"""
    if args.service == "ssh":
        brute_forcer = SSHBruteForce()

        if args.username and args.password_list:
            # Single username with password list
            brute_forcer.brute_force_single(args.target, args.username, args.password_list)
        elif args.credentials_list:
            # Username:password pairs from a file
            brute_forcer.brute_force_multiple(args.target, args.credentials_list)
        elif args.usernames_list and args.password_list:
            # Dictionary attack with separate username and password lists
            brute_forcer.dictionary_attack(args.target, args.usernames_list, args.password_list)
        else:
            print(f"{Fore.RED}[!] Error: Invalid combination of arguments for brute force attack{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[*] Use one of the following combinations:{Style.RESET_ALL}")
            print(f"    - --username and --password-list")
            print(f"    - --credentials-list")
            print(f"    - --usernames-list and --password-list")

def launch_gui():
    """Launch the graphical user interface"""
    try:
        # Import the GUI module
        from gui import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"{Fore.RED}[!] Error: Could not import GUI module: {str(e)}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] Make sure you have tkinter installed.{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}[!] Error launching GUI: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)

def main():
    """Main function"""
    print_banner()

    parser = setup_argparse()
    args = parser.parse_args()

    if args.command == "gui":
        launch_gui()
    elif args.command == "scan":
        handle_scan_command(args)
    elif args.command == "brute":
        handle_brute_command(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Operation cancelled by user{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Fore.RED}[!] An error occurred: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)