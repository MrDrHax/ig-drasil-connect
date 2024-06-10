# Script to build and update the server 

echo "Updating server..."

git pull

echo "Pull complete"

# Build the front-end

cd "Front End/Connect Front"

echo "Building front-end..."

# build
npm install
npm run build

# move the build to /var/www/html

sudo cp -r dist/* /var/www/html/

cd ../../

# copy configs

echo "Copying configs..."

sudo cp -r nginx/* /etc/nginx/sites-available/
sudo cp -r systemd/* /etc/systemd/system/

# Build the back-end

# restart systemd service

echo "Building back-end..."

cd api
source venv/bin/activate
pip install -r requirements.txt

sudo systemctl restart connect

# restart nginx

echo "Restarting nginx..."

sudo systemctl restart nginx

# Done

echo "Server updated"