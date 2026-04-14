import psutil

def system_monitor():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    print(f"CPU: {cpu}%")
    print(f"RAM: {memory}%")
    print(f"Disk: {disk}%")

if __name__ == "__main__":
    system_monitor()