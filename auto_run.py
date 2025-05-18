#!/usr/bin/env python3
"""
Auto-Run Script for Penetration Testing Toolkit
This script automatically runs predefined scans and brute force attacks
"""

import os
import sys
import time
import argparse
import json
import logging
from datetime import datetime

# Add the parent directory to sys.path to allow importing modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our modules
from scanner.port_scanner import PortScanner
from brute_force.ssh_brute_force import SSHBruteForce

# Set up logging
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = os.path.join(log_dir, f"auto_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)

def load_config(config_file):
    """Load configuration from a JSON file"""
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        return config
    except Exception as e:
        logging.error(f"Error loading configuration: {str(e)}")
        sys.exit(1)

def run_port_scans(config):
    """Run port scans based on configuration"""
    try:
        scanner = PortScanner()
    except Exception as e:
        logging.error(f"Failed to initialize port scanner: {str(e)}")
        logging.error("Make sure nmap is installed and in your PATH")
        logging.error("You can download it from: https://nmap.org/download.html")
        return

    if 'port_scans' not in config:
        logging.warning("No port scans configured")
        return

    for scan in config['port_scans']:
        target = scan.get('target')
        ports = scan.get('ports', '1-1000')
        scan_type = scan.get('type', 'basic')

        if not target:
            logging.warning("Skipping scan with no target")
            continue

        logging.info(f"Starting {scan_type} scan on {target} for ports {ports}")

        try:
            if scan_type == 'basic':
                scanner.basic_scan(target, ports)
            elif scan_type == 'comprehensive':
                scanner.comprehensive_scan(target, ports)
            elif scan_type == 'stealth':
                scanner.stealth_scan(target, ports)
            else:
                logging.warning(f"Unknown scan type: {scan_type}, defaulting to basic")
                scanner.basic_scan(target, ports)

            # Add a delay between scans to avoid overwhelming the target
            time.sleep(2)

        except Exception as e:
            logging.error(f"Error during {scan_type} scan on {target}: {str(e)}")

def run_brute_force_attacks(config):
    """Run brute force attacks based on configuration"""
    try:
        brute_forcer = SSHBruteForce()
    except Exception as e:
        logging.error(f"Failed to initialize SSH brute forcer: {str(e)}")
        logging.error("Make sure all dependencies are installed")
        return

    if 'brute_force' not in config:
        logging.warning("No brute force attacks configured")
        return

    for attack in config['brute_force']:
        target = attack.get('target')
        port = attack.get('port', 22)
        attack_type = attack.get('type')

        if not target:
            logging.warning("Skipping brute force attack with no target")
            continue

        # Set the SSH port
        brute_forcer.port = port

        logging.info(f"Starting brute force attack on {target}:{port}")

        try:
            if attack_type == 'single_user':
                username = attack.get('username')
                password_list = attack.get('password_list')

                if not username or not password_list:
                    logging.warning("Missing username or password list for single user attack")
                    continue

                if not os.path.exists(password_list):
                    logging.warning(f"Password list not found: {password_list}")
                    continue

                logging.info(f"Running single user brute force with username '{username}'")
                brute_forcer.brute_force_single(target, username, password_list)

            elif attack_type == 'credentials_list':
                credentials_list = attack.get('credentials_list')

                if not credentials_list:
                    logging.warning("Missing credentials list for credentials list attack")
                    continue

                if not os.path.exists(credentials_list):
                    logging.warning(f"Credentials list not found: {credentials_list}")
                    continue

                logging.info(f"Running credentials list brute force")
                brute_forcer.brute_force_multiple(target, credentials_list)

            elif attack_type == 'dictionary_attack':
                usernames_list = attack.get('usernames_list')
                password_list = attack.get('password_list')

                if not usernames_list or not password_list:
                    logging.warning("Missing usernames list or password list for dictionary attack")
                    continue

                if not os.path.exists(usernames_list):
                    logging.warning(f"Usernames list not found: {usernames_list}")
                    continue

                if not os.path.exists(password_list):
                    logging.warning(f"Password list not found: {password_list}")
                    continue

                logging.info(f"Running dictionary attack")
                brute_forcer.dictionary_attack(target, usernames_list, password_list)

            else:
                logging.warning(f"Unknown attack type: {attack_type}")
                continue

            # Add a delay between attacks to avoid overwhelming the target
            time.sleep(2)

        except Exception as e:
            logging.error(f"Error during brute force attack on {target}: {str(e)}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Auto-Run Script for Penetration Testing Toolkit")
    parser.add_argument("--config", "-c", default="config.json", help="Path to configuration file (default: config.json)")
    args = parser.parse_args()

    logging.info("Starting Auto-Run Script")

    # Load configuration
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), args.config)
    logging.info(f"Loading configuration from {config_path}")
    config = load_config(config_path)

    # Run port scans
    if config.get('enable_port_scans', True):
        logging.info("Running port scans")
        run_port_scans(config)

    # Run brute force attacks
    if config.get('enable_brute_force', True):
        logging.info("Running brute force attacks")
        run_brute_force_attacks(config)

    logging.info("Auto-Run Script completed")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        sys.exit(1)
