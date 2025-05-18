# Penetration Testing Toolkit

A toolkit for network scanning and brute force attacks, designed for security professionals and penetration testers. Includes both command-line and graphical user interfaces.

## Features

- **Port Scanning**: Utilizes nmap to perform various types of port scans
  - Basic scan: Simple port scanning with service detection
  - Comprehensive scan: Full port scanning with OS detection and service fingerprinting
  - Stealth scan: SYN scanning with reduced detection footprint

- **SSH Brute Force**: Attempts to brute force SSH login credentials
  - Single username with password list
  - Multiple username/password combinations from a credentials file
  - Dictionary attack with separate username and password lists

- **Graphical User Interface**: Easy-to-use GUI for all toolkit features
  - Tabbed interface for different tools
  - Results viewer
  - File selection dialogs
  - Automatic screenshot capture of results

- **Screenshot Functionality**: Captures and saves screenshots of scan and brute force results
  - Automatically saves screenshots when operations complete
  - Stores screenshots in a configurable directory outside the project
  - Organizes screenshots by date and operation type

## Dependencies

- Python 3.6+
- nmap (must be installed separately)
- Python packages: python-nmap, paramiko, colorama, tqdm

### Handling Missing Dependencies

The toolkit will check for required dependencies and provide helpful messages if they are missing:

- **Missing nmap**: If nmap is not installed or not in your PATH, the Port Scanner tab will show an error message with a "Download nmap" button that opens the nmap download page.

- **Missing Python packages**: If required Python packages are missing, the SSH Brute Force tab will show an error message with an "Install Dependencies" button that will attempt to install the packages using pip.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/pen_test_toolkit.git
   cd pen_test_toolkit
   ```

2. Create a virtual environment (recommended):
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Install nmap:
   - Windows: Download and install from [nmap.org](https://nmap.org/download.html#windows)
   - Linux: `sudo apt install nmap` (Ubuntu/Debian) or `sudo yum install nmap` (CentOS/RHEL)
   - macOS: `brew install nmap` (using Homebrew)

## Usage

### Launcher

The easiest way to start the toolkit is to use the launcher:
```
python launcher.py
```

Or simply double-click the `PenTestToolkit.bat` file on Windows.

The launcher provides a simple menu to choose which mode to run the toolkit in:
- GUI Mode: Launch the graphical user interface
- Auto-Run Mode: Run predefined scans and brute force attacks
- Command-Line Help: Show help for command-line usage

### Graphical User Interface

Launch the GUI:
```
python main.py gui
```

The GUI provides an intuitive interface for all toolkit features:
- Port Scanner tab: Configure and run nmap scans
- SSH Brute Force tab: Configure and run brute force attacks
- Results tab: View and manage scan/brute force results

### Command-Line Interface

#### Port Scanning

Basic scan:
```
python main.py scan 192.168.1.1 --type basic --ports 1-1000
```

Comprehensive scan:
```
python main.py scan 192.168.1.1 --type comprehensive
```

Stealth scan:
```
python main.py scan 192.168.1.1 --type stealth --ports 22,80,443
```

#### SSH Brute Force

Single username with password list:
```
python main.py brute 192.168.1.1 --username admin --password-list wordlists/passwords.txt
```

Using a credentials list (username:password format):
```
python main.py brute 192.168.1.1 --credentials-list wordlists/credentials.txt
```

Dictionary attack with separate username and password lists:
```
python main.py brute 192.168.1.1 --usernames-list wordlists/usernames.txt --password-list wordlists/passwords.txt
```

### Automatic Execution

The toolkit can be run automatically with predefined settings using the auto-run script:

```
python auto_run.py
```

Or simply double-click the `auto_run.bat` file on Windows.

#### Configuration

Automatic execution is controlled by the `config.json` file, which defines:
- Which targets to scan
- What port ranges to use
- Which scan types to perform
- What brute force attacks to attempt

Example configuration:
```json
{
    "enable_port_scans": true,
    "enable_brute_force": true,
    "port_scans": [
        {
            "target": "192.168.1.1",
            "ports": "22-80",
            "type": "basic"
        }
    ],
    "brute_force": [
        {
            "target": "192.168.1.1",
            "port": 22,
            "type": "single_user",
            "username": "admin",
            "password_list": "wordlists/passwords.txt"
        }
    ]
}
```

#### Scheduling

On Windows, you can schedule the automatic execution using the provided PowerShell script:

```
powershell -ExecutionPolicy Bypass -File schedule_task.ps1
```

This will create a scheduled task to run the toolkit daily at 2 AM. You can modify the schedule in Task Scheduler.

## Results

All scan and brute force results are saved in the `results` directory:
- Port scan results are saved as JSON files
- Brute force results are saved as text files

## Screenshots

The toolkit automatically captures screenshots of scan and brute force results:

- **Location**: Screenshots are saved to `~/PenTest_Screenshots` by default
- **Organization**: Screenshots are organized by date in subdirectories (e.g., `2023-05-19/`)
- **Naming**: Files are named with operation type, target, and timestamp (e.g., `port_scan_192.168.1.1_basic_20230519_120530.png`)

### Screenshot Features

- **Automatic Screenshots**: Captured when scans or brute force attacks complete
- **Manual Screenshots**: Take screenshots of the entire application window using the "Take Screenshot" button
- **Custom Directory**: Change the screenshot directory through the GUI
- **Open Screenshots**: Easily open the screenshot directory from the GUI

### Accessing Screenshots

1. In the GUI, go to the "Results" tab
2. The screenshot directory is displayed at the top
3. Click "Browse" to change the directory
4. Click "Open Folder" to view the screenshots in your file explorer

## Troubleshooting

### "nmap is not installed or not found in PATH"

If you see this error in the Port Scanner tab:

1. **Install nmap**:
   - Click the "Download nmap" button in the GUI, or
   - Download from [nmap.org](https://nmap.org/download.html)

2. **Ensure nmap is in your PATH**:
   - During installation, make sure to select the option to add nmap to your system PATH
   - If you've already installed nmap, you may need to add its installation directory to your PATH manually

3. **Restart the application** after installing nmap

### "Required dependencies for SSH brute force are not available"

If you see this error in the SSH Brute Force tab:

1. **Install required packages**:
   - Click the "Install Dependencies" button in the GUI, or
   - Run `pip install paramiko colorama tqdm` in your command prompt

2. **Restart the application** after installing the packages

### Other Issues

If you encounter other issues:

1. **Check the logs directory** for detailed error messages
2. **Ensure you have the correct permissions** to run network scans and connect to SSH servers
3. **Verify your target is reachable** using ping or other network tools

## Disclaimer

This tool is provided for educational and professional security testing purposes only. Always ensure you have explicit permission to scan or attempt to access the target systems. Unauthorized scanning or access attempts may be illegal in your jurisdiction.

## License

This project is licensed under the MIT License - see the LICENSE file for details.#   P e n i t r a t i o n _ t e s t i n g _ t o o l k i t  
 