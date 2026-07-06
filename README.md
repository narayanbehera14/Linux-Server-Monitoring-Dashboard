# Linux Server Monitor

A Linux server monitoring dashboard built with Bash, HTML, CSS, Docker, Jenkins, and AWS EC2.

- Live Demo: http://23.23.147.41:8080
- GitHub: https://github.com/narayanbehera14/Linux-Server-Monitoring-Dashboard

## Project Structure

```
linux-server-monitor/
├── monitor.sh
├── report.html
├── style.css
├── nginx-site.conf
├── README.md
├── logs/
└── screenshots/
```


                | Layer            | Technology       |
| ---------------- | ---------------- |
| Cloud            | AWS EC2          |
| Operating System | Ubuntu Linux     |
| Version Control  | Git & GitHub     |
| CI/CD            | Jenkins          |
| Containerization | Docker           |
| Web Server       | Nginx            |
| Frontend         | HTML, CSS        |
| Automation       | Jenkinsfile      |
| Deployment       | Docker Container |

Linux Server Monitoring Dashboard – DevOps Architecture

                    +----------------------+
                    |      Developer       |
                    | (Narayan Behera)     |
                    +----------+-----------+
                               |
                               | git push
                               |
                               ▼
                    +----------------------+
                    |       GitHub         |
                    | Linux Server Monitor |
                    |   Source Repository  |
                    +----------+-----------+
                               |
                               | Webhook / Poll SCM
                               |
                               ▼
                +--------------------------------+
                |        Jenkins Pipeline         |
                |   Running in Docker Container   |
                |      Port : 9090               |
                +---------------+----------------+
                                |
                                |
               Stage 1 : Clone Repository
                                |
               Stage 2 : Build Docker Image
                                |
               Stage 3 : Remove Old Container
                                |
               Stage 4 : Deploy New Container
                                |
                                ▼
                    +------------------------+
                    |      Docker Engine      |
                    |     (AWS EC2 Host)      |
                    +-----------+------------+
                                |
                                |
                      Runs Docker Container
                                |
                                ▼
                  +----------------------------+
                  | Linux Monitor Container     |
                  |       Nginx Server          |
                  | report.html                |
                  | style.css                  |
                  | Port : 8080               |
                  +-------------+-------------+
                                |
                                |
                                ▼
                    +------------------------+
                    |       End Users         |
                    | Browser                |
                    | http://EC2-IP:8080     |
                    +------------------------+


#AWS Infrastructure

                     AWS Cloud
                         │
                         │
                +------------------+
                |     EC2 Ubuntu    |
                |   t2.micro/t3.micro|
                +---------+---------+
                          │
      ┌───────────────────┼──────────────────┐
      │                   │                  │
      ▼                   ▼                  ▼
 Docker Engine       Jenkins Container   Linux Monitor
 Port 2375          Port 9090           Container
                                        Port 8080

#CI/CD Pipeline Flow
Developer
    │
    │ git push
    ▼
GitHub Repository
    │
    ▼
Jenkins Pipeline
    │
    ├── Clone Repository
    │
    ├── Build Docker Image
    │
    ├── Remove Old Container
    │
    ├── Run New Container
    │
    ▼
Docker Engine
    │
    ▼
Linux Monitor Container
    │
    ▼
Application Available
http://44.197.188.251:8080


           Jenkins Pipeline Workflow

           Pipeline

↓

Checkout Source Code

↓

Clone GitHub Repository

↓

Build Docker Image

↓

Delete Existing Container
(if exists)

↓

Create New Container

↓

Deploy Application

↓

Pipeline Success

              
## Architecture

This project is designed to collect Linux system information, render it as a static HTML dashboard, and optionally serve it via Nginx.

### Layers

- **Data collection**
  - `monitor.sh` runs Linux tools like `free`, `df`, `uptime`, `ps`, `who`, `hostname`, and `date`.
  - Command output is formatted into `report.html` and also saved as a timestamped log in `logs/`.

- **Presentation**
  - `report.html` is the generated dashboard view.
  - `style.css` provides the dashboard styling.

- **Automation / Deployment**
  - `cron` can run `monitor.sh` every minute to keep the dashboard updated automatically.
  - `nginx-site.conf` is a sample Nginx configuration to serve the dashboard at `http://localhost`.

### Optional DevOps Extension

This repository can be extended into a full CI/CD pipeline with tools like Git, Jenkins, Docker, and Nginx. In that case:

- source code is pushed to GitHub,
- Jenkins builds and deploys a container,
- Docker runs the app,
- Nginx serves the dashboard.

## What It Shows

- CPU usage and load
- RAM usage
- Disk usage
- System uptime
- Logged-in users
- Top processes
- Hostname
- Date & time

## Usage

1. Make the script executable:
   ```bash
   chmod +x monitor.sh
   ```

2. Run the script:
   ```bash
   ./monitor.sh
   ```

3. Open `report.html` in your browser.

4. Each run also saves a timestamped log in `logs/`.

## Cron Automation

To run the dashboard automatically every minute, add a crontab entry for your user.

```bash
crontab -e
```

Then add:

```bash
*/1 * * * * /home/liju/linux-server-monitor/monitor.sh >/dev/null 2>&1
```

This keeps `report.html` and logs updated every minute.

## Host with Nginx

You can serve the dashboard locally via Nginx so it is accessible at `http://localhost`.

1. Install Nginx (Debian/Parrot):
   ```bash
   sudo apt update
   sudo apt install -y nginx
   ```

2. Copy the sample site config and enable it:
   ```bash
   sudo cp nginx-site.conf /etc/nginx/sites-available/linux-server-monitor
   sudo ln -s /etc/nginx/sites-available/linux-server-monitor /etc/nginx/sites-enabled/
   ```

3. Ensure Nginx can read the files (adjust if your user/home differs):
   ```bash
   sudo chown -R www-data:www-data /home/liju/linux-server-monitor
   sudo chmod -R 755 /home/liju/linux-server-monitor
   ```

4. Test and reload Nginx:
   ```bash
   sudo nginx -t
   sudo systemctl reload nginx
   ```

5. Open your browser at `http://localhost` or `http://<your-ip>`.

## Screenshots

Add dashboard screenshots to the `screenshots/` folder for documentation or portfolio use.

## Notes

- `monitor.sh` uses standard Linux utilities and writes a static HTML report.
- `style.css` controls the dashboard appearance.
- `logs/` contains timestamped log files from each run.

## Next Steps

- Automate updates with cron
- Serve the dashboard via Nginx
- Add Docker and CI/CD integration for deployment

```bash
sudo cp nginx-site.conf /etc/nginx/sites-available/linux-server-monitor
sudo ln -s /etc/nginx/sites-available/linux-server-monitor /etc/nginx/sites-enabled/
```

3. Ensure Nginx can read the files (adjust if your user/home differs):

```bash
sudo chown -R www-data:www-data /home/liju/linux-server-monitor
sudo chmod -R 755 /home/liju/linux-server-monitor
```

4. Test and reload Nginx:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

5. Open your browser at `http://localhost` or `http://<your-ip>`.

Notes:
- If you prefer not to change ownership, you can instead adjust the `root` path in the site config to a directory Nginx already serves.
- To keep the dashboard updated automatically, ensure the cron entry is installed for the same user that owns the files (or run the script as root in cron).
