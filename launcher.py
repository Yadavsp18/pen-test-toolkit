#!/usr/bin/env python3
"""
Launcher for Penetration Testing Toolkit
Provides a simple menu to choose which mode to run the toolkit in
"""

import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox

def run_command(command):
    """Run a command and return the process"""
    try:
        if sys.platform == 'win32':
            # On Windows, use shell=True to run in a new window
            return subprocess.Popen(command, shell=True)
        else:
            # On Unix-like systems, use a list of arguments
            return subprocess.Popen(command.split())
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run command: {str(e)}")
        return None

class LauncherApp:
    """Launcher application for the Penetration Testing Toolkit"""
    
    def __init__(self, root):
        """Initialize the launcher"""
        self.root = root
        self.root.title("Penetration Testing Toolkit Launcher")
        self.root.geometry("500x400")
        self.root.minsize(500, 400)
        
        # Set icon if available
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Penetration Testing Toolkit", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Description
        desc_text = "Choose a mode to launch the toolkit:"
        desc_label = ttk.Label(main_frame, text=desc_text, wraplength=400)
        desc_label.pack(pady=10)
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # GUI mode button
        gui_button = ttk.Button(buttons_frame, text="GUI Mode", command=self.launch_gui, width=20)
        gui_button.pack(pady=10)
        
        # Auto-run mode button
        auto_button = ttk.Button(buttons_frame, text="Auto-Run Mode", command=self.launch_auto_run, width=20)
        auto_button.pack(pady=10)
        
        # Command-line mode button
        cli_button = ttk.Button(buttons_frame, text="Command-Line Help", command=self.show_cli_help, width=20)
        cli_button.pack(pady=10)
        
        # Exit button
        exit_button = ttk.Button(main_frame, text="Exit", command=root.destroy, width=20)
        exit_button.pack(pady=10)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def launch_gui(self):
        """Launch the GUI mode"""
        self.status_var.set("Launching GUI mode...")
        process = run_command("python main.py gui")
        if process:
            self.status_var.set("GUI mode launched")
    
    def launch_auto_run(self):
        """Launch the auto-run mode"""
        self.status_var.set("Launching Auto-Run mode...")
        process = run_command("python auto_run.py")
        if process:
            self.status_var.set("Auto-Run mode launched")
    
    def show_cli_help(self):
        """Show command-line help"""
        self.status_var.set("Showing command-line help...")
        process = run_command("python main.py --help")
        if process:
            self.status_var.set("Command-line help displayed")

def main():
    """Main function"""
    root = tk.Tk()
    app = LauncherApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
