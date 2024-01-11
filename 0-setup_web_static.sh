#!/usr/bin/env bash
# Install Nginx if not already installed
sudo apt-get update
sudo apt-get install nginx -y

# Create necessary directories
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Create a fake HTML file for testing
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Create or recreate the symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user and group recursively
sudo chown -R $USER:$USER /data/

# Update Nginx configuration
nginx_config="/etc/nginx/sites-available/default"
nginx_alias="location /hbnb_static {\n    alias /data/web_static/current/;\n    index index.html index.htm;\n}\n"
grep -qF "$nginx_alias" "$nginx_config" || echo -e "$nginx_alias" | sudo tee -a "$nginx_config"

# Restart Nginx
sudo service nginx restart
