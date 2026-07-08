from flask import Flask, jsonify, render_template
import psutil
import socket
import platform
import time
import subprocess
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/metrics")
def metrics():

    start = time.time()

    # Hostname
    hostname = socket.gethostname()

    # Private IP
    try:
        private_ip = socket.gethostbyname(hostname)
    except:
        private_ip = "Unavailable"

    # Public IP
    try:
        public_ip = requests.get(
            "https://ifconfig.me/ip",
            timeout=3
        ).text.strip()
    except:
        public_ip = "Unavailable"

    # CPU
    cpu = psutil.cpu_percent(interval=0.5)

    # RAM
    memory = psutil.virtual_memory().percent

    # Disk
    disk = psutil.disk_usage("/")

    disk_percent = disk.percent
    disk_total = round(disk.total / (1024 ** 3), 2)
    disk_used = round(disk.used / (1024 ** 3), 2)
    disk_free = round(disk.free / (1024 ** 3), 2)

    # OS
    os_name = platform.platform()

    # Uptime
    boot_time = psutil.boot_time()
    uptime_seconds = int(time.time() - boot_time)

    days = uptime_seconds // 86400
    hours = (uptime_seconds % 86400) // 3600
    minutes = (uptime_seconds % 3600) // 60

    uptime = f"{days}d {hours}h {minutes}m"

    # Docker Containers
    try:
        containers = subprocess.getoutput(
            "docker ps --format '{{.Names}}'"
        ).splitlines()

        if containers == ['']:
            containers = []
    except:
        containers = []

    # Connected Users
    try:
        users = subprocess.getoutput("who").splitlines()
        connected_users = len(users)
    except:
        connected_users = 0

    # Response Time
    response_time = round((time.time() - start) * 1000, 2)

    # Last Updated
    last_updated = time.strftime("%I:%M:%S %p")

    return jsonify({

        "hostname": hostname,

        "private_ip": private_ip,

        "public_ip": public_ip,

        "os": os_name,

        "cpu": cpu,

        "memory": memory,

        "disk_percent": disk_percent,

        "disk_total": disk_total,

        "disk_used": disk_used,

        "disk_free": disk_free,

        "uptime": uptime,

        "docker_running": len(containers),

        "docker_containers": containers,

        "connected_users": connected_users,

        "response_time": response_time,

        "last_updated": last_updated

    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)