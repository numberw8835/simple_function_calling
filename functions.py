functions = [
    {
        "name": "get_current_time",
        "description": "Gets the current system time in HH:MM:SS format.",
        "parameters": {}
    },
    {
        "name": "get_hostname",
        "description": "Retrieves the machine's hostname.",
        "parameters": {}
    },
    {
        "name": "get_uptime",
        "description": "Gets the system uptime in seconds since last boot.",
        "parameters": {}
    },
    {
        "name": "list_users",
        "description": "Lists all users currently registered on the system.",
        "parameters": {}
    },
    {
        "name": "get_disk_usage",
        "description": "Returns total, used, and free disk space (in GB) along with usage percentage.",
        "parameters": {}
    },
    {
        "name": "list_processes",
        "description": "Provides a list of currently running processes with their PID, name, and associated username.",
        "parameters": {}
    },
    {
        "name": "get_cpu_usage",
        "description": "Gets the current CPU utilization percentage.",
        "parameters": {}
    },
    {
        "name": "get_ip_address",
        "description": "Fetches the machine's IP address (or 127.0.0.1 if not connected).",
        "parameters": {}
    },
    {
        "name": "check_internet_connection",
        "description": "Checks whether the machine has an active internet connection.",
        "parameters": {}
    },
    {
        "name": "scan_network",
        "description": "Scans the local network (192.168.1.0/24) for open SSH (port 22) using Nmap.",
        "parameters": {}
    },
    {
        "name": "get_ram_info",
        "description": "Returns the total RAM available on the system in gigabytes (GB).",
        "parameters": {}
    },
    {
        "name": "get_system_info",
        "description": "Provides comprehensive system information including CPU cores, RAM, swap, disk partitions, and network statistics.",
        "parameters": {}
    },
    {
        "name": "list_installed_packages",
        "description": "Lists all software packages installed on the system using the Pacman package manager.",
        "parameters": {}
    },
    {
        "name": "open_terminal",
        "description": "Opens a new Zsh terminal session.",
        "parameters": {}
    },
    {
        "name": "restart_pc",
        "description": "Restarts the computer immediately.",
        "parameters": {}
    },
    {
        "name": "greet_user",
        "description": "Greets the user with welcome message.",
        "parameters": {
            "user_name": ""
        }
    },
    {
        "name": "reverse_string",
        "description": "Reverse string",
        "parameters": {
            "input_string": ""
        }
    },
    {
        "name": "collatz_sequence",
        "description": "Returns the Collatz sequence for a given number.",
        "parameters": {
            "n": "integer"
        }
    },
    {
        "name": "hack_fbi",
        "description": "Simulates a harmless 'hack' on the FBI by changing the user's screen color to red.",
        "parameters": {
            "name": "string"
        }
    }
]
