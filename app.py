from flask import Flask, jsonify, render_template
import psutil
import socket
import platform
import time

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/metrics")
def metrics():

    boot_time = psutil.boot_time()
    uptime_seconds = int(time.time() - boot_time)

    hours = uptime_seconds // 3600
    minutes = (uptime_seconds % 3600) // 60

    uptime = f"{hours} hours {minutes} minutes"

    return jsonify({
        "hostname": socket.gethostname(),
        "cpu": psutil.cpu_percent(interval=0.5),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage("/").percent,
        "os": platform.platform(),
        "uptime": uptime
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)