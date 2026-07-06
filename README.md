# Linux Server Monitor

A Linux server monitoring dashboard built with Bash, HTML, and CSS.

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

## Architecture

This project is designed as a simple monitoring dashboard with three main layers:

- **Data collection**
  - `monitor.sh` runs native Linux commands (`free`, `df`, `uptime`, `ps`, `who`, `hostname`, `date`) and formats the output.
  - The script generates the HTML dashboard file and saves a timestamped log in `logs/` for audit/history.

- **Presentation**
  - `report.html` is the generated dashboard that displays system status information.
  - `style.css` provides visual styling for the dashboard UI.

- **Deployment / Automation**
  - `cron` can run `monitor.sh` every minute to refresh `report.html` automatically.
  - `nginx-site.conf` is a sample Nginx configuration that serves the dashboard at `http://localhost`.

This architecture keeps the data pipeline simple while demonstrating monitoring, scheduling, and web deployment.

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

## Add a screenshot

Put dashboard screenshots in the `screenshots/` folder if you want to include them in the repo.

## Notes

- The script uses native Linux utilities like `free`, `df`, `ps`, `who`, and `top`.
- `monitor.sh` generates a fresh `report.html` every time it runs.
- `style.css` controls the dashboard appearance.

## Next steps

- Automate updates with Cron
- Host the report using Nginx
- Push the project to GitHub as a portfolio repository

## Cron Automation

To run the dashboard automatically every minute, add a crontab entry for your user. Edit your crontab:

```bash
crontab -e
```

Then add the following line (adjust the path if your project is in a different location):

```
*/1 * * * * /home/liju/linux-server-monitor/monitor.sh >/dev/null 2>&1
```

This will run the script every minute and keep `report.html` and a timestamped log in `logs/` up to date.

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

Notes:
- If you prefer not to change ownership, you can instead adjust the `root` path in the site config to a directory Nginx already serves.
- To keep the dashboard updated automatically, ensure the cron entry is installed for the same user that owns the files (or run the script as root in cron).
