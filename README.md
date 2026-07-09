 # Linux Server Monitor

 A lightweight, real-time server monitoring dashboard built with Flask. Designed to run inside a Docker container on an EC2 instance (or locally) and provide live system metrics (CPU, memory, disk, uptime, hostname, OS) via a simple JSON API and a responsive browser UI.

 Table of Contents
 - [Overview](#overview)
 - [Features](#features)
 - [Project Structure](#project-structure)
 - [Quick Start](#quick-start)
 - [Docker Deployment](#docker-deployment)
 - [AWS + Jenkins Deployment](#aws--jenkins-deployment)
 - [Metrics API](#metrics-api)
 - [Troubleshooting](#troubleshooting)
 - [Contributing](#contributing)
 - [License](#license)


## Overview

This project exposes a `/metrics` JSON endpoint and a single-page dashboard that polls metrics every 5 seconds. It is useful for quick visibility into a Linux host (for demos, labs, or small deployments).


## Architecture

High-level architecture and data flow:

```
   Browser (UI) <--polls-- Flask app (container) <--reads-- Host OS (/host)
     ^                          |
     |                          v
   /metrics JSON endpoint     Docker on EC2
                 |
                 v
              Jenkins (CI) -> builds Docker image
```

- `Flask` serves `index.html` and exposes `/metrics` which returns JSON.
- Client-side JavaScript polls `/metrics` every 5s and updates the UI.
- Running in Docker: container can mount the host filesystem at `/host` to read real host metrics.
- `Jenkins` (optional) builds and deploys the Docker image to the EC2 host.

Notes:
- If not running in Docker, the app reads metrics from the local filesystem and system APIs.
- The `/host` mount is read-only in Docker runs (`-v /:/host:ro`) for safety.


### Expanded architecture (network, ports, security, deployment)

- Components:
  - Browser (client UI)
  - Flask application (inside Docker container)
  - Host OS (metrics source, optionally mounted at `/host`)
  - Jenkins (CI) — optional build/deploy
  - (Optional) Docker registry or image repo

- Network & Ports:
  - `Flask` default (if run directly): `127.0.0.1:5000` inside host.
  - Docker container commonly exposes port `80` and maps to host `80` or `8080` (`-p HOST:CONTAINER`).
  - Jenkins typically runs on `8080`/`9090` (if used); SSH on `22` for EC2 management.
  - If using a private Docker registry, port `5000` may be used.

- Security best practices:
  - Run the container with the host filesystem mounted read-only: `-v /:/host:ro`.
  - Avoid running the app as root inside the container; use a non-root user where possible.
  - Use AWS Security Groups to restrict inbound traffic to required ports (HTTP/HTTPS and SSH for admin).
  - Terminate TLS at a load balancer or reverse proxy (ALB/NGINX) and keep the app on HTTP internally.
  - Enable minimal logging retention and rotate logs (`/var/log/...`) to avoid disk exhaustion.
  - For private dashboards, restrict access via IP allowlists, VPN, or basic auth.

- Deployment flow (recommended):
  1. Developer pushes to GitHub.
  2. Jenkins builds and publishes Docker image (optional registry).
  3. Target EC2 pulls the image (or Jenkins deploys) and runs the container.
  4. Use a simple update strategy: start new container, verify health, stop old container (or use a load balancer for zero-downtime).

- Operational notes:
  - Health: add a lightweight `/health` endpoint if you plan to use a load balancer or orchestration.
  - Monitoring: ship container logs to a centralized service (CloudWatch, ELK) for diagnosis.
  - Backups: dashboard is read-only; only persistence concerns are logs and any saved screenshots.

This expanded section should help plan networking, hardening, and deployment choices.


## Tech Stack & Workflow

Tech stack (recommended):

- Backend: `Flask` (Python) + `psutil`
- Containerization: `Docker`
- CI/CD: `Jenkins` (optional)
- Hosting: AWS EC2 (or any VM/container host)
- Optional registry: Docker Hub / private registry
- Monitoring/logs: CloudWatch / ELK / Promtail + Loki

Simple workflow diagram:

```
 Developer  -->  GitHub (repo)
  |                |
  |  push           |  webhook / poll
  v                v
   Jenkins (CI) ----> Docker registry (optional)
     |                  |
     | build & push     | pull
     v                  v
   EC2 host (Docker) --> Container: Flask app
          |  reads metrics from /host (read-only)
          v
          Browser UI polls /metrics every 5s
```

Step-by-step runtime flow:

1. Developer pushes code to GitHub.
2. Jenkins (if used) checks out repo, runs tests, builds Docker image and (optionally) pushes it to a registry.
3. The EC2 host pulls the image (or Jenkins deploys directly) and runs the container.
4. Container runs `app.py`; if mounted with `-v /:/host:ro` it reads host metrics via `/host`.
5. Flask exposes `/metrics` which returns JSON containing cpu, memory, disk, hostname, os, uptime.
6. Browser loads `index.html` and client JS polls `/metrics` every 5 seconds to update the dashboard.
7. Logs are written to local `logs/` inside container or shipped to a log service for retention and analysis.

Ports and endpoints to consider:

- `80` (HTTP) or `443` (HTTPS) — host-facing port mapped to container port (commonly 80).
- `5000` — Flask default when running without a production front-end (internal).
- `/metrics` — JSON endpoint for metrics; consider `/health` for simple health checks.

Security & operational tips:

- Use a minimal base image and a non-root user in Docker.
- Use IAM roles and Security Groups to limit access to EC2.
- Automate image builds and deployments with CI, and use health checks to verify new containers before switching traffic.



## Features

- Real-time metrics (5s polling)
- CPU, memory, and disk usage
- Hostname, OS, and uptime
- Responsive dark-themed UI
- Runs in Docker and suitable for small EC2 instances (t2.micro+)
- Optional Jenkins pipeline for automated builds and deployment


## Project Structure

```
linux-server-monitor/
├── app.py
├── requirements.txt
├── Dockerfile
├── Jenkinsfile
├── templates/index.html
├── static/style.css
├── monitor.sh          # legacy utility (archived)
├── README.md
├── logs/
└── screenshots/
```


## Quick Start

Local development:

```bash
git clone https://github.com/narayanbehera14/Linux-Server-Monitoring-Dashboard.git
cd linux-server-monitor
pip install -r requirements.txt
python app.py
# Open: http://localhost/
```


## Docker Deployment

Build and run:

```bash
docker build -t linux-monitor:latest .
docker run -d \
  --name linux-monitor \
  --restart unless-stopped \
  -p 80:80 \
  -v /:/host:ro \
  linux-monitor:latest
# Open: http://localhost:80 (or http://HOST_IP)
```

Note: Mounting `/` into the container at `/host` (read-only) lets the app read real host metrics. If `/host` is not mounted it will fall back to reading from the container filesystem.


## AWS + Jenkins Deployment

Typical flow:

1. Push changes to GitHub.
2. Jenkins pipeline builds a Docker image and deploys it on the target EC2 host.

Ensure Docker is installed on the EC2 host and the Jenkins job uses the included `Jenkinsfile`.


## Metrics API

Fetch metrics:

```bash
curl http://localhost/metrics
```

Example response:

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

The dashboard polls this endpoint every 5 seconds and updates the UI.


## Troubleshooting

- Disk or metrics show 0%: make sure you ran the container with `-v /:/host:ro` so the app can query the host filesystem.
- Port conflict on 80: run the container on another host port, e.g. `-p 8080:80` and visit `http://localhost:8080`.
- Metrics API unavailable: verify the container is running and reachable, check container logs (e.g. `docker logs linux-monitor`).


## Contributing

Contributions are welcome. Fork the repo, make changes, and open a pull request.


## License

MIT License


## Author

Narayan Behera — DevOps & AWS Engineering

---

If you'd like, I can also:
- add a concise Table of Contents links to each major section (already included),
- update the `README` to remove the hard-coded public IP demo link, or
- create a short `README` badge set (build, docker pulls).
