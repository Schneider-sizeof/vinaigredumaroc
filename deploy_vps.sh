#!/bin/bash
set -e

echo "=========================================================="
echo "      Vinaigre du Maroc — VPS Deployment Script"
echo "=========================================================="

# 1. Update packages
echo "[1/8] Updating Ubuntu system packages..."
sudo apt update && sudo apt upgrade -y

# 2. Install dependencies
echo "[2/8] Installing Nginx, Python, Git, and Certbot..."
sudo apt install -y python3-pip python3-venv nginx git certbot python3-certbot-nginx

# 3. Configure folder permissions
echo "[3/8] Creating directory /var/www and setting permissions..."
sudo mkdir -p /var/www
sudo chown -R $USER:$USER /var/www

# 4. Clone or pull repository
cd /var/www
if [ -d "vinaigredumaroc" ]; then
    echo "Directory /var/www/vinaigredumaroc already exists. Pulling latest main branch..."
    cd vinaigredumaroc
    git fetch --all
    git reset --hard origin/main
else
    echo "Cloning repository..."
    git clone https://github.com/Schneider-sizeof/vinaigredumaroc.git
    cd vinaigredumaroc
fi

# 5. Set up virtual environment and install requirements
echo "[4/8] Creating virtual environment and installing python dependencies..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn

# 6. Configure environment variables
echo "[5/8] Creating .env file..."
cat <<EOF > .env
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(50))")
DEBUG=False
SITE_URL=https://vinaigredumaroc.com
DB_ENGINE=sqlite3
ROBOTS_DISALLOW_ALL=False
EOF

# 7. Database migrations, updates, and staticfiles collection
echo "[6/8] Running migrations and database configurations..."
python manage.py migrate --noinput
python update_db_translations.py
python populate_db.py
python manage.py collectstatic --noinput

# 8. Create systemd Gunicorn service
echo "[7/8] Configuring Gunicorn daemon systemd service..."
cat <<EOF > /tmp/gunicorn.service
[Unit]
Description=gunicorn daemon for Vinaigre du Maroc
After=network.target

[Service]
User=$USER
Group=www-data
WorkingDirectory=/var/www/vinaigredumaroc
ExecStart=/var/www/vinaigredumaroc/venv/bin/gunicorn \\
          --access-logfile - \\
          --workers 3 \\
          --bind unix:/run/gunicorn.sock \\
          vinaigre_project.wsgi:application

[Install]
WantedBy=multi-user.target
EOF
sudo mv /tmp/gunicorn.service /etc/systemd/system/gunicorn.service

# 9. Create Nginx site configuration
echo "[8/8] Configuring Nginx reverse proxy..."
cat <<EOF > /tmp/vinaigredumaroc
server {
    listen 80;
    server_name vinaigredumaroc.com www.vinaigredumaroc.com;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /media/ {
        root /var/www/vinaigredumaroc;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
EOF
sudo mv /tmp/vinaigredumaroc /etc/nginx/sites-available/vinaigredumaroc

# Link site config and remove default
sudo ln -sf /etc/nginx/sites-available/vinaigredumaroc /etc/nginx/sites-enabled/
if [ -f /etc/nginx/sites-enabled/default ]; then
    sudo rm -f /etc/nginx/sites-enabled/default
fi

# Reload systemd and restart services
echo "Starting and enabling services..."
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl restart gunicorn
sudo systemctl restart nginx

echo "=========================================================="
echo " Deployment Successful!"
echo "=========================================================="
echo "Next step: Run the following command to set up SSL:"
echo "  sudo certbot --nginx -d vinaigredumaroc.com -d www.vinaigredumaroc.com"
echo "=========================================================="
