#!/usr/bin/env python3
"""
Screenshot Utility for Penetration Testing Toolkit
Captures and saves screenshots of the GUI results
"""

import os
import sys
import time
from datetime import datetime
import tkinter as tk
from PIL import ImageGrab, Image

# Default screenshot directory (outside the project)
DEFAULT_SCREENSHOT_DIR = os.path.join(os.path.expanduser("~"), "PenTest_Screenshots")

class ScreenshotUtil:
    """Utility class for capturing and saving screenshots"""
    
    def __init__(self, screenshot_dir=None):
        """
        Initialize the screenshot utility
        
        Args:
            screenshot_dir (str, optional): Directory to save screenshots. 
                                           Defaults to ~/PenTest_Screenshots.
        """
        self.screenshot_dir = screenshot_dir or DEFAULT_SCREENSHOT_DIR
        
        # Create the screenshot directory if it doesn't exist
        if not os.path.exists(self.screenshot_dir):
            try:
                os.makedirs(self.screenshot_dir)
                print(f"Created screenshot directory: {self.screenshot_dir}")
            except Exception as e:
                print(f"Error creating screenshot directory: {str(e)}")
                # Fall back to the current directory
                self.screenshot_dir = os.path.join(os.getcwd(), "screenshots")
                if not os.path.exists(self.screenshot_dir):
                    os.makedirs(self.screenshot_dir)
    
    def capture_window(self, window, title=None, operation_type=None):
        """
        Capture a screenshot of a specific tkinter window
        
        Args:
            window (tk.Toplevel or tk.Tk): The window to capture
            title (str, optional): Custom title for the screenshot
            operation_type (str, optional): Type of operation (scan, brute_force, etc.)
            
        Returns:
            str: Path to the saved screenshot file, or None if failed
        """
        try:
            # Ensure the window is on top and fully updated
            window.lift()
            window.update_idletasks()
            window.update()
            
            # Give the window a moment to fully render
            time.sleep(0.5)
            
            # Get window geometry
            x = window.winfo_rootx()
            y = window.winfo_rooty()
            width = window.winfo_width()
            height = window.winfo_height()
            
            # Capture the screenshot
            screenshot = ImageGrab.grab(bbox=(x, y, x+width, y+height))
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            operation_type = operation_type or "result"
            title = title or "screenshot"
            filename = f"{operation_type}_{title}_{timestamp}.png"
            
            # Create subdirectory based on date
            date_dir = os.path.join(self.screenshot_dir, datetime.now().strftime("%Y-%m-%d"))
            if not os.path.exists(date_dir):
                os.makedirs(date_dir)
            
            # Save the screenshot
            filepath = os.path.join(date_dir, filename)
            screenshot.save(filepath)
            
            print(f"Screenshot saved to: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"Error capturing screenshot: {str(e)}")
            return None
    
    def capture_widget(self, widget, title=None, operation_type=None):
        """
        Capture a screenshot of a specific tkinter widget
        
        Args:
            widget (tk.Widget): The widget to capture
            title (str, optional): Custom title for the screenshot
            operation_type (str, optional): Type of operation (scan, brute_force, etc.)
            
        Returns:
            str: Path to the saved screenshot file, or None if failed
        """
        try:
            # Ensure the widget is updated
            widget.update_idletasks()
            
            # Get widget geometry
            x = widget.winfo_rootx()
            y = widget.winfo_rooty()
            width = widget.winfo_width()
            height = widget.winfo_height()
            
            # Capture the screenshot
            screenshot = ImageGrab.grab(bbox=(x, y, x+width, y+height))
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            operation_type = operation_type or "widget"
            title = title or "screenshot"
            filename = f"{operation_type}_{title}_{timestamp}.png"
            
            # Create subdirectory based on date
            date_dir = os.path.join(self.screenshot_dir, datetime.now().strftime("%Y-%m-%d"))
            if not os.path.exists(date_dir):
                os.makedirs(date_dir)
            
            # Save the screenshot
            filepath = os.path.join(date_dir, filename)
            screenshot.save(filepath)
            
            print(f"Widget screenshot saved to: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"Error capturing widget screenshot: {str(e)}")
            return None
    
    def get_screenshot_dir(self):
        """Get the current screenshot directory"""
        return self.screenshot_dir
    
    def set_screenshot_dir(self, directory):
        """
        Set a new screenshot directory
        
        Args:
            directory (str): New directory path
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
            
            self.screenshot_dir = directory
            return True
        except Exception as e:
            print(f"Error setting screenshot directory: {str(e)}")
            return False


# Example usage
if __name__ == "__main__":
    # Create a test window
    root = tk.Tk()
    root.title("Screenshot Test")
    root.geometry("400x300")
    
    label = tk.Label(root, text="This is a test window for screenshots")
    label.pack(pady=20)
    
    button = tk.Button(root, text="Take Screenshot", 
                      command=lambda: ScreenshotUtil().capture_window(root, "test", "example"))
    button.pack(pady=20)
    
    root.mainloop()
