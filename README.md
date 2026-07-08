# Linux Server Monitor

A real-time EC2 monitoring dashboard built with Flask, Python, Docker, Jenkins, and AWS EC2. Displays live system metrics with automatic 5-second refresh.

**🌐 Live Demo:** http://23.23.147.41:8080  
**📂 GitHub:** https://github.com/narayanbehera14/Linux-Server-Monitoring-Dashboard

## Project Structure

```
linux-server-monitor/
├── app.py                    # Flask application - metrics API & dashboard
├── requirements.txt          # Python dependencies (Flask, psutil)
├── templates/
│   └── index.html           # Dashboard UI
├── static/
│   └── style.css            # Modern dark theme styling
├── Dockerfile               # Container configuration
├── Jenkinsfile              # CI/CD pipeline
├── monitor.sh               # Legacy shell script (archived)
├── nginx-site.conf          # Nginx config (legacy)
├── README.md
├── logs/                    # Monitor logs
└── screenshots/             # Dashboard screenshots
```

## Technology Stack

| Layer            | Technology       |
|------------------|------------------|
| Cloud            | AWS EC2          |
| OS               | Ubuntu Linux     |
| Version Control  | Git & GitHub     |
| CI/CD            | Jenkins          |
| Containerization | Docker           |
| Backend          | Flask (Python)   |
| Frontend         | HTML, CSS, JS    |
| Metrics API      | `/metrics` JSON  |
| System Insights  | psutil, subprocess|
| Deployment       | Docker Container |

## Architecture Overview

### Deployment Pipeline

```
Developer (Git Push)
    ↓
GitHub Repository
    ↓
Jenkins (Webhook/Poll)
    ├── Clone Repo
    ├── Build Docker Image
    ├── Remove Old Container
    └── Run New Container
    ↓
Docker Engine (AWS EC2)
    ↓
Flask Application (Port 80)
    ├── GET /          → index.html
    └── GET /metrics   → JSON (cpu, ram, disk, hostname, os, uptime)
    ↓
Browser (Client)
    ↓
JavaScript (5-second polling)
    ↓
Live Dashboard Updates
```

### Container Architecture

```
AWS EC2 Instance
    │
    ├── Docker Engine
    │   │
    │   └── Flask Container (Port 80)
    │       ├── /app/app.py
    │       ├── /app/templates/index.html
    │       ├── /app/static/style.css
    │       ├── /app/requirements.txt
    │       ├── /host/         (mounted EC2 root filesystem)
    │       └── Python 3.12 Runtime
    │
    ├── Jenkins Container (Port 9090) - CI/CD
    │
    └── EC2 Root Filesystem (/)
        ├── System Metrics (CPU, RAM, Disk)
        ├── Hostname, OS Info
        └── Uptime
```

## Features

✅ **Real-time Metrics** - Updates every 5 seconds without page refresh  
✅ **Live EC2 Metrics** - CPU, RAM, Disk usage from the actual host  
✅ **Responsive Design** - Works on desktop, tablet, mobile  
✅ **Modern UI** - Dark theme with progress bars and smooth animations  
✅ **System Information** - Hostname, OS version, uptime  
✅ **Zero Downtime Deployment** - Jenkins auto-replaces old container  
✅ **Auto-scaling Ready** - Lightweight, runs on t2.micro or larger  

## Metrics Endpoint

The application exposes a JSON API for real-time metrics:

```bash
curl http://localhost/metrics
```

Response:
```json
{
  "hostname": "ip-172-31-8-194",
  "cpu": 21.5,
  "memory": 43.2,
  "disk": 31.8,
  "os": "Linux-7.0.0-1006-aws-x86_64-with-glibc2.41",
  "uptime": "2d 2h 20m"
}
```

## What It Shows

- **CPU Usage** - Real-time percentage (0-100%)
- **RAM Usage** - Memory consumption percentage
- **Disk Usage** - Root filesystem or mounted `/host` filesystem
- **Hostname** - EC2 instance hostname
- **OS** - Linux kernel and distribution info
- **Uptime** - How long the instance has been running
- **Last Updated** - Timestamp of the last metrics fetch

All metrics update automatically every 5 seconds.

## How It Works

### Backend (Flask)

`app.py` runs a Flask server that:

1. **Serves the dashboard** at `/` (index.html)
2. **Exposes a metrics API** at `/metrics` (JSON endpoint)
3. **Collects system data** using `psutil` and `subprocess`
4. **Returns JSON** with current system metrics

### Frontend (JavaScript)

`templates/index.html` with vanilla JavaScript:

1. **Fetches `/metrics`** every 5 seconds
2. **Updates the DOM** with new values
3. **Animates progress bars** for visual feedback
4. **Shows last-updated timestamp**
5. **No page refresh** required (seamless experience)

### Deployment (Docker)

The `Dockerfile`:
- Uses `python:3.12-slim` base image
- Installs Flask and psutil from `requirements.txt`
- Mounts the EC2 root filesystem at `/host` for real metrics
- Runs Flask on port 80 (accessible from outside)

### CI/CD (Jenkins)

The `Jenkinsfile`:
- Listens for GitHub pushes
- Builds a new Docker image
- Stops the old container
- Runs the new container
- Zero-downtime deployment

## Quick Start

### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/narayanbehera14/Linux-Server-Monitoring-Dashboard.git
   cd linux-server-monitor
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Flask app:**
   ```bash
   python app.py
   ```

4. **Open your browser:**
   ```
   http://localhost/
   ```

   The dashboard will display live metrics and refresh every 5 seconds.

### Docker Deployment

1. **Build the Docker image:**
   ```bash
   docker build -t linux-monitor:latest .
   ```

2. **Run the container:**
   ```bash
   docker run -d \
     --name linux-monitor \
     --restart unless-stopped \
     -p 80:80 \
     -v /:/host:ro \
     linux-monitor:latest
   ```

   This mounts the EC2 root filesystem as read-only at `/host` so the app can read real metrics.

3. **Access the dashboard:**
   ```
   http://localhost:80
   ```

### AWS EC2 Deployment with Jenkins

1. **Create an EC2 instance** (t2.micro or larger):
   - Install Docker: `sudo apt install -y docker.io`
   - Add user to docker group: `sudo usermod -aG docker $USER`
   - Install Git: `sudo apt install -y git`

2. **Set up Jenkins** (runs alongside the monitor in another container or on the host)

3. **Configure a Jenkins pipeline job:**
   - Point to this GitHub repository
   - Use the `Jenkinsfile` from the repo
   - Set up a webhook in GitHub: `https://your-jenkins-url/github-webhook/`

4. **Trigger a build:**
   - Push code to GitHub
   - Jenkins automatically builds and deploys the container
   - Dashboard is live at `http://EC2-IP:80`

## File Reference

| File | Purpose |
|------|---------|
| `app.py` | Flask application, metrics API, dashboard server |
| `requirements.txt` | Python dependencies (Flask, psutil) |
| `templates/index.html` | Dashboard HTML UI |
| `static/style.css` | Responsive dark theme styling |
| `Dockerfile` | Container image definition |
| `Jenkinsfile` | CI/CD pipeline stages |
| `monitor.sh` | Legacy Bash script (archived, no longer used) |
| `nginx-site.conf` | Legacy Nginx config (archived, no longer used) |

## Troubleshooting

### Container can't access EC2 metrics

**Problem:** Disk shows 0% or metrics are incorrect

**Solution:** Ensure Docker mounts the root filesystem:
```bash
docker run -d ... -v /:/host:ro linux-monitor:latest
```

The app reads from `/host/` when available, otherwise falls back to `/`.

### Port 80 already in use

**Problem:** `Address already in use`

**Solution:** Use a different port:
```bash
docker run -d -p 8080:80 ... linux-monitor:latest
# Then access: http://localhost:8080
```

Or stop the conflicting service:
```bash
sudo systemctl stop nginx
```

### Metrics API returns "Unavailable"

**Problem:** Public IP or hostname not found

**Solution:** This is expected inside Docker. The app gracefully handles network limitations:
- Private IP: Retrieved from `hostname -I`
- Public IP: Fetched from `ifconfig.me` (requires internet)
- Hostname: Reads from `/etc/hostname` (falls back to `socket.gethostname()`)

## Performance & Scalability

- **Lightweight:** Flask + psutil, minimal dependencies
- **CPU:** ~1-2% per instance
- **Memory:** ~50MB per container
- **Startup:** <2 seconds
- **Response time:** <100ms per metrics fetch
- **Refresh rate:** 5-second client-side polling (adjustable)

Perfect for:
- EC2 t2.micro (free tier)
- Kubernetes pods
- ARM-based edge devices
- Portfolio projects

## Future Enhancements

- [ ] Historical metrics storage (database)
- [ ] Grafana/Prometheus integration
- [ ] Alert thresholds (email/Slack)
- [ ] Multi-instance monitoring
- [ ] Docker container status
- [ ] Jenkins pipeline status
- [ ] WebSocket for real-time updates
- [ ] Export metrics to CSV

## Contributing

Fork, improve, and submit pull requests!

## License

MIT License - Feel free to use this project as a learning resource or portfolio piece.

## Author

**Narayan Behera** - DevOps & AWS Engineering

---

**Made with ❤️ for AWS & DevOps Engineers**
