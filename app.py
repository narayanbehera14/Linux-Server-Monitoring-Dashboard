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

    # =========================
    # EC2 Hostname
    # =========================
    try:
        with open("/host/etc/hostname", "r") as f:
            hostname = f.read().strip()
    except Exception:
        hostname = socket.gethostname()

    # =========================
    # Private IP
    # =========================
    try:
        private_ip = subprocess.check_output(
            "hostname -I | awk '{print $1}'",
            shell=True
        ).decode().strip()
    except Exception:
        private_ip = "Unavailable"

    # =========================
    # Public IP
    # =========================
    try:
        public_ip = requests.get(
            "https://ifconfig.me/ip",
            timeout=3
        ).text.strip()
    except Exception:
        public_ip = "Unavailable"

    # =========================
    # CPU Usage
    # =========================
    cpu = psutil.cpu_percent(interval=0.5)

    # =========================
    # Memory Usage
    # =========================
    memory = psutil.virtual_memory().percent

    # =========================
    # Disk Usage (Host EC2 Disk)
    # =========================
    try:
        disk = psutil.disk_usage("/host")
    except Exception:
        disk = psutil.disk_usage("/")

    disk_percent = disk.percent
    disk_total = round(disk.total / (1024 ** 3), 2)
    disk_used = round(disk.used / (1024 ** 3), 2)
    disk_free = round(disk.free / (1024 ** 3), 2)

    # =========================
    # Operating System
    # =========================
    os_name = platform.platform()

    # =========================
    # Uptime
    # =========================
    boot_time = psutil.boot_time()
    uptime_seconds = int(time.time() - boot_time)

    days = uptime_seconds // 86400
    hours = (uptime_seconds % 86400) // 3600
    minutes = (uptime_seconds % 3600) // 60

    uptime = f"{days}d {hours}h {minutes}m"

    # =========================
    # Running Docker Containers
    # =========================
    try:
        containers = subprocess.check_output(
            "docker ps --format '{{.Names}}'",
            shell=True
        ).decode().splitlines()
    except Exception:
        containers = []

    # =========================
    # Connected Users
    # =========================
    try:
        connected_users = len(
            subprocess.check_output("who", shell=True).decode().splitlines()
        )
    except Exception:
        connected_users = 0

    # =========================
    # Response Time
    # =========================
    response_time = round((time.time() - start) * 1000, 2)

    # =========================
    # Last Updated
    # =========================
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