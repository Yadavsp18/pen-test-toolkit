#!/usr/bin/env python3
"""
Penetration Testing Toolkit - GUI Module
A graphical user interface for the penetration testing toolkit
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import threading
import queue
import io
import webbrowser
from contextlib import redirect_stdout
from datetime import datetime

# Add the parent directory to sys.path to allow importing modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our modules
from scanner.port_scanner import PortScanner
from brute_force.ssh_brute_force import SSHBruteForce
from utils.screenshot_util import ScreenshotUtil

class RedirectText:
    """Class to redirect stdout to a tkinter Text widget"""
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.queue = queue.Queue()
        self.updating = True
        threading.Thread(target=self.update_text_widget, daemon=True).start()

    def write(self, string):
        self.queue.put(string)

    def flush(self):
        pass

    def update_text_widget(self):
        while self.updating:
            try:
                while True:
                    text = self.queue.get_nowait()
                    self.text_widget.configure(state='normal')
                    self.text_widget.insert(tk.END, text)
                    self.text_widget.see(tk.END)
                    self.text_widget.configure(state='disabled')
                    self.queue.task_done()
            except queue.Empty:
                pass
            self.text_widget.update_idletasks()
            import time
            time.sleep(0.1)

    def close(self):
        self.updating = False

class PenTestToolkitGUI:
    """Main GUI class for the Penetration Testing Toolkit"""

    def __init__(self, root):
        """Initialize the GUI"""
        self.root = root
        self.root.title("Penetration Testing Toolkit")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)

        # Set icon if available
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass

        # Create results directory if it doesn't exist
        self.results_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)

        # Initialize screenshot utility
        # Default location is ~/PenTest_Screenshots
        self.screenshot_util = ScreenshotUtil()
        self.screenshot_dir = self.screenshot_util.get_screenshot_dir()

        # Initialize scanner and brute forcer
        try:
            self.scanner = PortScanner()
            self.brute_forcer = SSHBruteForce()
        except Exception as e:
            messagebox.showerror("Initialization Error",
                               f"Error initializing tools: {str(e)}\n\n"
                               f"Make sure nmap is installed and in your PATH.\n"
                               f"You can download it from: https://nmap.org/download.html")
            # Set to None so we can check later
            self.scanner = None
            self.brute_forcer = None

        # Create the main notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create tabs
        self.scan_tab = ttk.Frame(self.notebook)
        self.brute_tab = ttk.Frame(self.notebook)
        self.results_tab = ttk.Frame(self.notebook)
        self.about_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.scan_tab, text="Port Scanner")
        self.notebook.add(self.brute_tab, text="SSH Brute Force")
        self.notebook.add(self.results_tab, text="Results")
        self.notebook.add(self.about_tab, text="About")

        # Initialize tabs
        self.init_scan_tab()
        self.init_brute_tab()
        self.init_results_tab()
        self.init_about_tab()

        # Create status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def init_scan_tab(self):
        """Initialize the Port Scanner tab"""
        # Create frames
        input_frame = ttk.LabelFrame(self.scan_tab, text="Scan Settings")
        input_frame.pack(fill=tk.X, padx=10, pady=10)

        output_frame = ttk.LabelFrame(self.scan_tab, text="Scan Output")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Target input
        ttk.Label(input_frame, text="Target:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.scan_target_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.scan_target_var, width=30).grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        # Port range input
        ttk.Label(input_frame, text="Ports:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.scan_ports_var = tk.StringVar(value="1-1000")
        ttk.Entry(input_frame, textvariable=self.scan_ports_var, width=15).grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)

        # Scan type selection
        ttk.Label(input_frame, text="Scan Type:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.scan_type_var = tk.StringVar(value="basic")
        scan_types = ["basic", "comprehensive", "stealth"]
        ttk.Combobox(input_frame, textvariable=self.scan_type_var, values=scan_types, state="readonly", width=15).grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        # Scan button
        self.scan_button = ttk.Button(input_frame, text="Start Scan", command=self.start_scan)
        self.scan_button.grid(row=1, column=3, padx=5, pady=5, sticky=tk.E)

        # Output text area
        self.scan_output = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, height=20)
        self.scan_output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.scan_output.configure(state='disabled')

        # Check if nmap is available
        if self.scanner is None:
            self.scan_output.configure(state='normal')
            self.scan_output.insert(tk.END, "ERROR: nmap is not installed or not found in PATH.\n\n")
            self.scan_output.insert(tk.END, "To use the port scanner, please install nmap:\n")
            self.scan_output.insert(tk.END, "1. Download from: https://nmap.org/download.html\n")
            self.scan_output.insert(tk.END, "2. Install and ensure it's added to your system PATH\n")
            self.scan_output.insert(tk.END, "3. Restart this application\n\n")

            # Add a download button
            download_frame = ttk.Frame(output_frame)
            download_frame.pack(pady=10)
            download_button = ttk.Button(download_frame, text="Download nmap",
                                        command=lambda: self.open_url("https://nmap.org/download.html"))
            download_button.pack()

            self.scan_output.configure(state='disabled')
            self.scan_button.configure(state='disabled')

    def init_brute_tab(self):
        """Initialize the SSH Brute Force tab"""
        # Create frames
        input_frame = ttk.LabelFrame(self.brute_tab, text="Brute Force Settings")
        input_frame.pack(fill=tk.X, padx=10, pady=10)

        output_frame = ttk.LabelFrame(self.brute_tab, text="Brute Force Output")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Target input
        ttk.Label(input_frame, text="Target:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.brute_target_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.brute_target_var, width=30).grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        # Port input
        ttk.Label(input_frame, text="Port:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.brute_port_var = tk.StringVar(value="22")
        ttk.Entry(input_frame, textvariable=self.brute_port_var, width=10).grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)

        # Attack type selection
        ttk.Label(input_frame, text="Attack Type:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.attack_type_var = tk.StringVar(value="single_user")
        attack_types = [("Single User", "single_user"),
                        ("Credentials List", "credentials_list"),
                        ("Dictionary Attack", "dictionary_attack")]

        attack_frame = ttk.Frame(input_frame)
        attack_frame.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky=tk.W)

        for i, (text, value) in enumerate(attack_types):
            ttk.Radiobutton(attack_frame, text=text, variable=self.attack_type_var, value=value,
                           command=self.update_brute_options).pack(side=tk.LEFT, padx=10)

        # Options frame that changes based on attack type
        self.brute_options_frame = ttk.LabelFrame(input_frame, text="Attack Options")
        self.brute_options_frame.grid(row=2, column=0, columnspan=4, padx=5, pady=5, sticky=tk.W+tk.E)

        # Single user options (default)
        self.username_var = tk.StringVar()
        self.password_list_var = tk.StringVar()
        self.credentials_list_var = tk.StringVar()
        self.usernames_list_var = tk.StringVar()

        # Initialize the options frame with single user options
        self.update_brute_options()

        # Brute force button
        self.brute_button = ttk.Button(input_frame, text="Start Brute Force", command=self.start_brute_force)
        self.brute_button.grid(row=3, column=3, padx=5, pady=5, sticky=tk.E)

        # Output text area
        self.brute_output = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, height=20)
        self.brute_output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.brute_output.configure(state='disabled')

        # Check if paramiko is available
        if self.brute_forcer is None:
            self.brute_output.configure(state='normal')
            self.brute_output.insert(tk.END, "ERROR: Required dependencies for SSH brute force are not available.\n\n")
            self.brute_output.insert(tk.END, "To use the SSH brute force feature, please ensure the following packages are installed:\n")
            self.brute_output.insert(tk.END, "1. paramiko\n")
            self.brute_output.insert(tk.END, "2. colorama\n")
            self.brute_output.insert(tk.END, "3. tqdm\n\n")
            self.brute_output.insert(tk.END, "You can install them using pip:\n")
            self.brute_output.insert(tk.END, "pip install paramiko colorama tqdm\n\n")
            self.brute_output.insert(tk.END, "Then restart this application.\n\n")

            # Add install button
            install_frame = ttk.Frame(output_frame)
            install_frame.pack(pady=10)
            install_button = ttk.Button(install_frame, text="Install Dependencies",
                                       command=self.install_dependencies)
            install_button.pack()

            self.brute_output.configure(state='disabled')
            self.brute_button.configure(state='disabled')

    def update_brute_options(self):
        """Update the brute force options based on the selected attack type"""
        # Clear the frame
        for widget in self.brute_options_frame.winfo_children():
            widget.destroy()

        attack_type = self.attack_type_var.get()

        if attack_type == "single_user":
            # Username input
            ttk.Label(self.brute_options_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
            ttk.Entry(self.brute_options_frame, textvariable=self.username_var, width=20).grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

            # Password list input
            ttk.Label(self.brute_options_frame, text="Password List:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
            password_frame = ttk.Frame(self.brute_options_frame)
            password_frame.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)

            ttk.Entry(password_frame, textvariable=self.password_list_var, width=30).pack(side=tk.LEFT, padx=0, pady=0)
            ttk.Button(password_frame, text="Browse", command=lambda: self.browse_file(self.password_list_var)).pack(side=tk.LEFT, padx=5, pady=0)

        elif attack_type == "credentials_list":
            # Credentials list input
            ttk.Label(self.brute_options_frame, text="Credentials List:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
            creds_frame = ttk.Frame(self.brute_options_frame)
            creds_frame.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky=tk.W)

            ttk.Entry(creds_frame, textvariable=self.credentials_list_var, width=50).pack(side=tk.LEFT, padx=0, pady=0)
            ttk.Button(creds_frame, text="Browse", command=lambda: self.browse_file(self.credentials_list_var)).pack(side=tk.LEFT, padx=5, pady=0)

        elif attack_type == "dictionary_attack":
            # Usernames list input
            ttk.Label(self.brute_options_frame, text="Usernames List:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
            usernames_frame = ttk.Frame(self.brute_options_frame)
            usernames_frame.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

            ttk.Entry(usernames_frame, textvariable=self.usernames_list_var, width=30).pack(side=tk.LEFT, padx=0, pady=0)
            ttk.Button(usernames_frame, text="Browse", command=lambda: self.browse_file(self.usernames_list_var)).pack(side=tk.LEFT, padx=5, pady=0)

            # Password list input
            ttk.Label(self.brute_options_frame, text="Password List:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
            password_frame = ttk.Frame(self.brute_options_frame)
            password_frame.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)

            ttk.Entry(password_frame, textvariable=self.password_list_var, width=30).pack(side=tk.LEFT, padx=0, pady=0)
            ttk.Button(password_frame, text="Browse", command=lambda: self.browse_file(self.password_list_var)).pack(side=tk.LEFT, padx=5, pady=0)

    def init_results_tab(self):
        """Initialize the Results tab"""
        # Create frames
        control_frame = ttk.Frame(self.results_tab)
        control_frame.pack(fill=tk.X, padx=10, pady=10)

        results_frame = ttk.LabelFrame(self.results_tab, text="Results Files")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Refresh button
        ttk.Button(control_frame, text="Refresh Results", command=self.refresh_results).pack(side=tk.LEFT, padx=5, pady=5)

        # Screenshot directory display and button
        screenshot_frame = ttk.Frame(control_frame)
        screenshot_frame.pack(side=tk.RIGHT, padx=5, pady=5)

        ttk.Label(screenshot_frame, text="Screenshots:").pack(side=tk.LEFT, padx=5)
        self.screenshot_dir_var = tk.StringVar(value=self.screenshot_dir)
        screenshot_entry = ttk.Entry(screenshot_frame, textvariable=self.screenshot_dir_var, width=30)
        screenshot_entry.pack(side=tk.LEFT, padx=5)

        ttk.Button(screenshot_frame, text="Browse",
                  command=self.browse_screenshot_dir).pack(side=tk.LEFT, padx=5)

        ttk.Button(screenshot_frame, text="Open Folder",
                  command=self.open_screenshot_dir).pack(side=tk.LEFT, padx=5)

        # Results listbox with scrollbar
        self.results_listbox_frame = ttk.Frame(results_frame)
        self.results_listbox_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.results_listbox = tk.Listbox(self.results_listbox_frame, selectmode=tk.SINGLE)
        self.results_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(self.results_listbox_frame, orient=tk.VERTICAL, command=self.results_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_listbox.config(yscrollcommand=scrollbar.set)

        # Bind double-click event to open result file
        self.results_listbox.bind("<Double-1>", self.open_result_file)

        # Button frame
        button_frame = ttk.Frame(results_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(button_frame, text="Open Selected", command=self.open_selected_result).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(button_frame, text="Delete Selected", command=self.delete_selected_result).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(button_frame, text="Take Screenshot", command=self.take_screenshot).pack(side=tk.LEFT, padx=5, pady=5)

        # Populate the results list
        self.refresh_results()

    def init_about_tab(self):
        """Initialize the About tab"""
        about_frame = ttk.Frame(self.about_tab)
        about_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Logo or banner (placeholder)
        logo_label = ttk.Label(about_frame, text="PENTEST TOOLKIT", font=("Arial", 24, "bold"))
        logo_label.pack(pady=20)

        # About text
        about_text = """
Penetration Testing Toolkit

A toolkit for network scanning and brute force attacks, designed for security professionals and penetration testers.

Features:
- Port Scanning: Utilizes nmap to perform various types of port scans
- SSH Brute Force: Attempts to brute force SSH login credentials

Disclaimer:
This tool is provided for educational and professional security testing purposes only.
Always ensure you have explicit permission to scan or attempt to access the target systems.
Unauthorized scanning or access attempts may be illegal in your jurisdiction.
"""
        about_label = ttk.Label(about_frame, text=about_text, justify=tk.CENTER, wraplength=600)
        about_label.pack(pady=10)

        # Version info
        version_label = ttk.Label(about_frame, text="Version 1.0.0", font=("Arial", 10))
        version_label.pack(pady=10)

    def browse_file(self, string_var):
        """Open a file browser dialog and set the selected file path to the given StringVar"""
        filename = filedialog.askopenfilename(
            title="Select a file",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        if filename:
            string_var.set(filename)

    def open_url(self, url):
        """Open a URL in the default web browser"""
        try:
            webbrowser.open(url)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open URL: {str(e)}")

    def install_dependencies(self):
        """Install required dependencies using pip"""
        try:
            # Show a message box to confirm
            confirm = messagebox.askyesno("Confirm Installation",
                                         "This will install the required dependencies (paramiko, colorama, tqdm) using pip. Continue?")
            if not confirm:
                return

            # Create a new window to show the installation progress
            install_window = tk.Toplevel(self.root)
            install_window.title("Installing Dependencies")
            install_window.geometry("500x300")
            install_window.transient(self.root)
            install_window.grab_set()

            # Add a text area to show the output
            output_text = scrolledtext.ScrolledText(install_window, wrap=tk.WORD)
            output_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            # Add a close button
            close_button = ttk.Button(install_window, text="Close", command=install_window.destroy)
            close_button.pack(pady=10)

            # Function to run the installation in a separate thread
            def run_installation():
                try:
                    import subprocess

                    # Run pip install
                    output_text.insert(tk.END, "Installing dependencies...\n\n")
                    process = subprocess.Popen(
                        [sys.executable, "-m", "pip", "install", "paramiko", "colorama", "tqdm"],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        universal_newlines=True
                    )

                    # Read the output
                    for line in process.stdout:
                        output_text.insert(tk.END, line)
                        output_text.see(tk.END)
                        output_text.update_idletasks()

                    # Wait for the process to complete
                    process.wait()

                    if process.returncode == 0:
                        output_text.insert(tk.END, "\n\nInstallation completed successfully.\n")
                        output_text.insert(tk.END, "Please restart the application to use the SSH brute force feature.\n")
                    else:
                        output_text.insert(tk.END, "\n\nInstallation failed. Please try installing manually:\n")
                        output_text.insert(tk.END, "pip install paramiko colorama tqdm\n")

                except Exception as e:
                    output_text.insert(tk.END, f"\n\nError during installation: {str(e)}\n")
                    output_text.insert(tk.END, "Please try installing manually:\n")
                    output_text.insert(tk.END, "pip install paramiko colorama tqdm\n")

            # Start the installation in a separate thread
            threading.Thread(target=run_installation, daemon=True).start()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to install dependencies: {str(e)}")

    def start_scan(self):
        """Start the port scanning process in a separate thread"""
        # Check if scanner is available
        if self.scanner is None:
            messagebox.showerror("Error", "Port scanner is not available. Make sure nmap is installed and in your PATH.")
            return

        target = self.scan_target_var.get().strip()
        ports = self.scan_ports_var.get().strip()
        scan_type = self.scan_type_var.get()

        if not target:
            messagebox.showerror("Error", "Please enter a target IP address or hostname.")
            return

        # Clear output
        self.scan_output.configure(state='normal')
        self.scan_output.delete(1.0, tk.END)
        self.scan_output.configure(state='disabled')

        # Redirect stdout to the text widget
        redirect = RedirectText(self.scan_output)
        sys.stdout = redirect

        # Disable the scan button
        self.scan_button.configure(state='disabled')
        self.status_var.set(f"Scanning {target}...")

        # Start scanning in a separate thread
        threading.Thread(target=self._run_scan, args=(target, ports, scan_type, redirect), daemon=True).start()

    def _run_scan(self, target, ports, scan_type, redirect):
        """Run the scan in a separate thread"""
        try:
            if scan_type == "basic":
                self.scanner.basic_scan(target, ports)
            elif scan_type == "comprehensive":
                self.scanner.comprehensive_scan(target, ports)
            elif scan_type == "stealth":
                self.scanner.stealth_scan(target, ports)

            # Take a screenshot of the scan results
            self.root.after(500, lambda: self._take_scan_screenshot(target, scan_type))

        except Exception as e:
            print(f"Error during scan: {str(e)}")
        finally:
            # Re-enable the scan button
            self.root.after(0, lambda: self.scan_button.configure(state='normal'))
            self.root.after(0, lambda: self.status_var.set("Ready"))
            self.root.after(0, lambda: self.refresh_results())

            # Restore stdout
            sys.stdout = sys.__stdout__
            redirect.close()

    def _take_scan_screenshot(self, target, scan_type):
        """Take a screenshot of the scan results"""
        try:
            # Switch to the scan tab to ensure it's visible
            self.notebook.select(0)  # 0 is the index of the scan tab

            # Take screenshot of the scan output
            filepath = self.screenshot_util.capture_widget(
                self.scan_output,
                f"{target}_{scan_type}",
                "port_scan"
            )

            if filepath:
                print(f"Scan screenshot saved to: {filepath}")
        except Exception as e:
            print(f"Error taking scan screenshot: {str(e)}")

    def start_brute_force(self):
        """Start the brute force process in a separate thread"""
        # Check if brute forcer is available
        if self.brute_forcer is None:
            messagebox.showerror("Error", "SSH Brute Force is not available. Make sure all dependencies are installed.")
            return

        target = self.brute_target_var.get().strip()
        attack_type = self.attack_type_var.get()

        if not target:
            messagebox.showerror("Error", "Please enter a target IP address or hostname.")
            return

        # Set the SSH port
        try:
            port = int(self.brute_port_var.get().strip())
            self.brute_forcer.port = port
        except ValueError:
            messagebox.showerror("Error", "Port must be a number.")
            return

        # Validate inputs based on attack type
        if attack_type == "single_user":
            username = self.username_var.get().strip()
            password_list = self.password_list_var.get().strip()

            if not username:
                messagebox.showerror("Error", "Please enter a username.")
                return

            if not password_list or not os.path.exists(password_list):
                messagebox.showerror("Error", "Please select a valid password list file.")
                return

        elif attack_type == "credentials_list":
            credentials_list = self.credentials_list_var.get().strip()

            if not credentials_list or not os.path.exists(credentials_list):
                messagebox.showerror("Error", "Please select a valid credentials list file.")
                return

        elif attack_type == "dictionary_attack":
            usernames_list = self.usernames_list_var.get().strip()
            password_list = self.password_list_var.get().strip()

            if not usernames_list or not os.path.exists(usernames_list):
                messagebox.showerror("Error", "Please select a valid usernames list file.")
                return

            if not password_list or not os.path.exists(password_list):
                messagebox.showerror("Error", "Please select a valid password list file.")
                return

        # Clear output
        self.brute_output.configure(state='normal')
        self.brute_output.delete(1.0, tk.END)
        self.brute_output.configure(state='disabled')

        # Redirect stdout to the text widget
        redirect = RedirectText(self.brute_output)
        sys.stdout = redirect

        # Disable the brute force button
        self.brute_button.configure(state='disabled')
        self.status_var.set(f"Brute forcing {target}...")

        # Start brute forcing in a separate thread
        threading.Thread(target=self._run_brute_force, args=(target, attack_type, redirect), daemon=True).start()

    def _run_brute_force(self, target, attack_type, redirect):
        """Run the brute force attack in a separate thread"""
        try:
            if attack_type == "single_user":
                username = self.username_var.get().strip()
                password_list = self.password_list_var.get().strip()
                self.brute_forcer.brute_force_single(target, username, password_list)

                # Take screenshot with attack details
                self.root.after(500, lambda: self._take_brute_force_screenshot(
                    target, attack_type, f"user_{username}"
                ))

            elif attack_type == "credentials_list":
                credentials_list = self.credentials_list_var.get().strip()
                self.brute_forcer.brute_force_multiple(target, credentials_list)

                # Take screenshot with attack details
                self.root.after(500, lambda: self._take_brute_force_screenshot(
                    target, attack_type, "creds_list"
                ))

            elif attack_type == "dictionary_attack":
                usernames_list = self.usernames_list_var.get().strip()
                password_list = self.password_list_var.get().strip()
                self.brute_forcer.dictionary_attack(target, usernames_list, password_list)

                # Take screenshot with attack details
                self.root.after(500, lambda: self._take_brute_force_screenshot(
                    target, attack_type, "dictionary"
                ))

        except Exception as e:
            print(f"Error during brute force attack: {str(e)}")

        finally:
            # Re-enable the brute force button
            self.root.after(0, lambda: self.brute_button.configure(state='normal'))
            self.root.after(0, lambda: self.status_var.set("Ready"))
            self.root.after(0, lambda: self.refresh_results())

            # Restore stdout
            sys.stdout = sys.__stdout__
            redirect.close()

    def _take_brute_force_screenshot(self, target, attack_type, details):
        """Take a screenshot of the brute force results"""
        try:
            # Switch to the brute force tab to ensure it's visible
            self.notebook.select(1)  # 1 is the index of the brute force tab

            # Take screenshot of the brute force output
            filepath = self.screenshot_util.capture_widget(
                self.brute_output,
                f"{target}_{attack_type}_{details}",
                "brute_force"
            )

            if filepath:
                print(f"Brute force screenshot saved to: {filepath}")
        except Exception as e:
            print(f"Error taking brute force screenshot: {str(e)}")

    def refresh_results(self):
        """Refresh the results list"""
        self.results_listbox.delete(0, tk.END)

        if os.path.exists(self.results_dir):
            files = sorted(os.listdir(self.results_dir), key=lambda x: os.path.getmtime(os.path.join(self.results_dir, x)), reverse=True)

            for file in files:
                self.results_listbox.insert(tk.END, file)

    def open_result_file(self, event):
        """Open the selected result file when double-clicked"""
        self.open_selected_result()

    def open_selected_result(self):
        """Open the selected result file"""
        selection = self.results_listbox.curselection()

        if selection:
            filename = self.results_listbox.get(selection[0])
            filepath = os.path.join(self.results_dir, filename)

            if os.path.exists(filepath):
                # Create a new window to display the file contents
                result_window = tk.Toplevel(self.root)
                result_window.title(f"Result: {filename}")
                result_window.geometry("800x600")

                # Text area for file contents
                text_area = scrolledtext.ScrolledText(result_window, wrap=tk.WORD)
                text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

                # Read and display the file contents
                try:
                    with open(filepath, 'r') as f:
                        content = f.read()
                        text_area.insert(tk.END, content)

                    text_area.configure(state='disabled')
                except Exception as e:
                    text_area.insert(tk.END, f"Error reading file: {str(e)}")

    def delete_selected_result(self):
        """Delete the selected result file"""
        selection = self.results_listbox.curselection()

        if selection:
            filename = self.results_listbox.get(selection[0])
            filepath = os.path.join(self.results_dir, filename)

            if os.path.exists(filepath):
                confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {filename}?")

                if confirm:
                    try:
                        os.remove(filepath)
                        self.refresh_results()
                    except Exception as e:
                        messagebox.showerror("Error", f"Could not delete file: {str(e)}")

    def browse_screenshot_dir(self):
        """Browse for a directory to save screenshots"""
        directory = filedialog.askdirectory(
            title="Select Screenshot Directory",
            initialdir=self.screenshot_dir
        )
        if directory:
            self.screenshot_dir_var.set(directory)
            self.screenshot_util.set_screenshot_dir(directory)
            self.screenshot_dir = directory

    def open_screenshot_dir(self):
        """Open the screenshot directory in the file explorer"""
        try:
            if os.path.exists(self.screenshot_dir):
                # Use webbrowser to open the directory
                webbrowser.open(f"file://{os.path.abspath(self.screenshot_dir)}")
            else:
                messagebox.showerror("Error", "Screenshot directory does not exist.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open screenshot directory: {str(e)}")

    def take_screenshot(self):
        """Take a screenshot of the current window"""
        try:
            # Take screenshot of the main window
            filepath = self.screenshot_util.capture_window(self.root, "main_window", "manual")

            if filepath:
                messagebox.showinfo("Screenshot", f"Screenshot saved to:\n{filepath}")

                # Ask if user wants to open the screenshot
                if messagebox.askyesno("Open Screenshot", "Do you want to open the screenshot?"):
                    # Use webbrowser to open the file
                    webbrowser.open(f"file://{os.path.abspath(filepath)}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not take screenshot: {str(e)}")

def main():
    """Main function to start the GUI"""
    root = tk.Tk()
    app = PenTestToolkitGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
