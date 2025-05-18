#!/usr/bin/env python3
"""
Port Scanner Module - Uses nmap to perform port scanning operations
"""

import nmap
import json
import os
from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class PortScanner:
    """
    A class that provides port scanning functionality using nmap
    """

    def __init__(self):
        """Initialize the port scanner"""
        self.scanner = nmap.PortScanner()
        self.results_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results")

        # Create results directory if it doesn't exist
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)

    def basic_scan(self, target, ports="1-1000"):
        """
        Perform a basic TCP scan on the specified target and ports

        Args:
            target (str): Target IP address or hostname
            ports (str): Port range to scan (default: "1-1000")

        Returns:
            dict: Scan results
        """
        try:
            print(f"{Fore.BLUE}[*] Starting basic scan on {target} for ports {ports}...{Style.RESET_ALL}")
            self.scanner.scan(target, ports, arguments="-sV")
            return self._process_results(target)
        except Exception as e:
            print(f"{Fore.RED}[!] Error during basic scan: {str(e)}{Style.RESET_ALL}")
            return None

    def comprehensive_scan(self, target, ports="1-65535"):
        """
        Perform a comprehensive scan with OS detection and version detection

        Args:
            target (str): Target IP address or hostname
            ports (str): Port range to scan (default: "1-65535")

        Returns:
            dict: Scan results
        """
        try:
            print(f"{Fore.BLUE}[*] Starting comprehensive scan on {target}...{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[*] This may take some time...{Style.RESET_ALL}")

            # -sS: TCP SYN scan, -sV: Version detection, -O: OS detection, -A: Enable OS detection, version detection, script scanning, and traceroute
            self.scanner.scan(target, ports, arguments="-sS -sV -O -A")
            return self._process_results(target)
        except Exception as e:
            print(f"{Fore.RED}[!] Error during comprehensive scan: {str(e)}{Style.RESET_ALL}")
            return None

    def stealth_scan(self, target, ports="1-1000"):
        """
        Perform a stealth scan (SYN scan) on the target

        Args:
            target (str): Target IP address or hostname
            ports (str): Port range to scan (default: "1-1000")

        Returns:
            dict: Scan results
        """
        try:
            print(f"{Fore.BLUE}[*] Starting stealth scan on {target}...{Style.RESET_ALL}")
            self.scanner.scan(target, ports, arguments="-sS -T2")
            return self._process_results(target)
        except Exception as e:
            print(f"{Fore.RED}[!] Error during stealth scan: {str(e)}{Style.RESET_ALL}")
            return None

    def _process_results(self, target):
        """
        Process and display scan results

        Args:
            target (str): The target that was scanned

        Returns:
            dict: Processed scan results
        """
        if target not in self.scanner.all_hosts():
            print(f"{Fore.RED}[!] No results found for {target}{Style.RESET_ALL}")
            return None

        results = {
            "target": target,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "scan_info": self.scanner[target],
        }

        # Display results
        print(f"\n{Fore.GREEN}[+] Scan Results for {target}:{Style.RESET_ALL}")

        # Check if host is up
        if self.scanner[target].state() == "up":
            print(f"{Fore.GREEN}[+] Host is up{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[!] Host appears to be down{Style.RESET_ALL}")
            return results

        # Display open ports and services
        for proto in self.scanner[target].all_protocols():
            print(f"\n{Fore.CYAN}Protocol: {proto}{Style.RESET_ALL}")

            ports = sorted(self.scanner[target][proto].keys())
            for port in ports:
                service = self.scanner[target][proto][port]
                state = service["state"]

                if state == "open":
                    service_name = service["name"] if "name" in service else "unknown"
                    product = service["product"] if "product" in service else ""
                    version = service["version"] if "version" in service else ""

                    service_info = f"{service_name}"
                    if product:
                        service_info += f" ({product}"
                        if version:
                            service_info += f" {version}"
                        service_info += ")"

                    print(f"{Fore.GREEN}[+] Port {port}/{proto}: {state} - {service_info}{Style.RESET_ALL}")

        # Save results to file
        self._save_results(results)

        return results

    def _save_results(self, results):
        """
        Save scan results to a JSON file

        Args:
            results (dict): Scan results to save
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        target = results["target"].replace(".", "_")
        filename = f"scan_{target}_{timestamp}.json"
        filepath = os.path.join(self.results_dir, filename)

        with open(filepath, "w") as f:
            json.dump(results, f, indent=4)

        print(f"\n{Fore.BLUE}[*] Results saved to {filepath}{Style.RESET_ALL}")


if __name__ == "__main__":
    # Example usage
    scanner = PortScanner()
    scanner.basic_scan("127.0.0.1", "22-80")