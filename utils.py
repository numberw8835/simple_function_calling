import psutil
import random

def get_weather(location):
    conditions = ["Sunny", "Cloudy", "Rainy", "Snowy", "Windy"]
    temperature = random.randint(-10, 40)  # Random temperature in Celsius
    condition = random.choice(conditions)
    return f"Current weather in {location}: {temperature}°C, {condition}"


def check_ram_size():
    """Returns the total RAM size in GB."""
    mem = psutil.virtual_memory()
    total_ram_gb = round(mem.total / (1024.0 ** 3), 2)
    return f"Total RAM: {total_ram_gb} GB"


def check_disk_size():
    """Returns the total and used disk size in GB for all mounted disks."""
    disk_info = []
    partitions = psutil.disk_partitions()
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            total_gb = round(usage.total / (1024.0 ** 3), 2)
            used_gb = round(usage.used / (1024.0 ** 3), 2)
            disk_info.append(f"{partition.device}: Total={total_gb} GB, Used={used_gb} GB")
        except PermissionError:
            disk_info.append(f"{partition.device}: (Permission Denied)")
    return "\n".join(disk_info)
