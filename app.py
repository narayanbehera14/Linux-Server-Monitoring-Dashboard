from flask import Flask, jsonify, render_template
import psutil
import socket
import platform
import subprocess

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/metrics")
def metrics():
    uptime = subprocess.check_output("uptime -p", shell=True).decode().strip()

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
