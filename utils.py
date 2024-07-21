import os
import socket
import subprocess
import psutil
from datetime import datetime
import requests


# --- System Information Functions ---
def get_current_time():
    """Gets the current time in HH:MM:SS format."""
    return datetime.now().strftime("%H:%M:%S")


def get_hostname():
    """Gets the machine's hostname."""
    return socket.gethostname()


def get_uptime():
    """Gets the system uptime in seconds."""
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
    return uptime_seconds


def list_users():
    """Lists all users on the system."""
    with open('/etc/passwd', 'r') as f:
        return [line.split(':')[0] for line in f]


def get_disk_usage():
    """Gets disk usage statistics (total, used, free, percent) in GB."""
    usage = psutil.disk_usage('/')
    return {
        "total": f"{usage.total / (1024 ** 3):.2f} GB",
        "used": f"{usage.used / (1024 ** 3):.2f} GB",
        "free": f"{usage.free / (1024 ** 3):.2f} GB",
        "percent": f"{usage.percent}%",
    }


def list_processes():
    """Lists currently running processes (PID, name, username)."""
    return [proc.info for proc in psutil.process_iter(['pid', 'name', 'username'])]


def get_cpu_usage():
    """Gets the current CPU usage percentage."""
    return psutil.cpu_percent(interval=1)  # Interval of 1 second for more accurate reading

def get_ip_address():
    """Gets the machine's IP address(es)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create a UDP socket
    try:
        # Doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def check_internet_connection():
    """Checks if connected to the internet by trying to connect to Google's DNS."""
    try:
        socket.create_connection(("8.8.8.8", 53))  # Google DNS
        return True
    except OSError:
        return False

def scan_network():
    """
    This function uses Nmap to scan the network for open SSH ports (port 22).
    It returns a string containing the results of the scan, including all hosts and their respective open ports.
    """
    command = ["nmap", "-sT", "--open", "-p", "22",
               "192.168.1.0/24"]  # Scanning network range 192.168.1.0 to 192.168.1.255
    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode == 0:
        return result.stdout
    else:
        return f"Error: {result.stderr}"


def get_ram_info():
    """Gets total RAM in GB."""
    total_memory_gb = psutil.virtual_memory().total / (1024 ** 3)
    return total_memory_gb


def get_system_info():
    """Retrieves comprehensive system information using psutil."""
    return {
        "cpu_count": psutil.cpu_count(logical=False),
        "cpu_logical_count": psutil.cpu_count(logical=True),
        "memory_total": get_ram_info(),  # Reuse get_ram_info for consistency
        "swap_total": psutil.swap_memory().total / (1024 ** 3),
        "disk_partitions": [part._asdict() for part in psutil.disk_partitions()],
        "net_io": psutil.net_io_counters()._asdict(),
    }


# --- Utility Functions ---

def list_installed_packages():
    """Lists installed packages using Pacman."""
    result = subprocess.run(['pacman', '-Q'], capture_output=True, text=True)
    return result.stdout.strip().split('\n') if result.returncode == 0 else []  # Return empty list on error


def open_terminal():
    """Opens a new Zsh terminal session."""
    subprocess.run(['zsh'])

def restart_pc():
    """
    Restarts the Linux computer by shutting down and then powering up the system.

    This function uses the 'shutdown' command with the '-r' option, which
    initiates a reboot of the machine. The parameter '-h +1' tells the system
    to shut down and restart after one minute. After waiting for the specified
    time (which is set to zero in this case), the system will perform the reboot.

    Description: This function restarts your Linux computer by scheduling a shutdown
    after which it will automatically restart the machine, allowing for an orderly
    shut down and startup process.
    """
    os.system('shutdown -r now')


def reverse_string(input_string: str) -> str:
    reversed_string = ''
    for char in input_string:
        reversed_string = char + reversed_string
    return reversed_string

def greet_user(user_name):
    """
    A simple function that greets the user by asking for their name and then prints a welcome message using that name.
    """

    return f"Welcome, {user_name}!"

def collatz_sequence(n):
    sequence = [n]
    while n > 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        sequence.append(n)
    sequence.append(1)
    return sequence