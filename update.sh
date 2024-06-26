# Script to build and update the server 

echo "Updating server..."

sudo chmod -R 777 /home/ubuntu/ig-drasil-connect/api
git pull

echo "Pull complete"

# Build the front-end

cd "Front End/Connect Front"

echo "Building front-end..."

# build
export NODE_ENV=production
sudo npm install
sudo npm run build

# move the build to /var/www/html

sudo cp -r dist/* /var/www/html/
sudo rm -r dist

cd ../../

# copy configs

echo "Copying configs..."

sudo cp -r nginx/* /etc/nginx/sites-enabled/
sudo cp -r systemd/* /etc/systemd/system/

sudo systemctl daemon-reload

# Build the back-end

# restart systemd service

echo "Building back-end..."

cd /home/ubuntu/ig-drasil-connect/api
/home/ubuntu/ig-drasil-connect/api/venv/bin/pip install -r requirements.txt
/home/ubuntu/ig-drasil-connect/api/venv/bin/pip install gunicorn

sudo chown www-data:www-data /home/ubuntu/ig-drasil-connect/api
sudo chmod -R 555 /home/ubuntu/ig-drasil-connect/api

sudo chown www-data:www-data /home/ubuntu/logs
sudo chmod -R 777 /home/ubuntu/logs

sudo systemctl restart connect

# restart nginx

echo "Restarting nginx..."

sudo certbot install --nginx -d connect.igdrasil.com
sudo systemctl reload nginx

# Done

echo "Server updated"
