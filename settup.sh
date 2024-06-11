# Setup the server to be ready for deployment

# asumes that nginx is already installed

# install npm and nodejs

echo "Setting up server..."

echo "Installing npm and nodejs..."

sudo apt-get install -y curl
curl -fsSL https://deb.nodesource.com/setup_22.x -o nodesource_setup.sh
sudo -E bash nodesource_setup.sh
sudo apt-get install -y nodejs
node -v

# install pip, venv and gunicorn

echo "Installing pip, venv and gunicorn..."

sudo apt install -y python3-pip python3-venv gunicorn3

# create venv

echo "Creating venv..."

cd api
python3 -m venv venv
cd ..

mkdir ../logs

# get certbot

echo "Installing certbot..."

sudo apt-get install -y certbot python3-certbot-nginx

sudo cp -r nginx/* /etc/nginx/sites-enabled/

# get the ssl certificate

echo "Getting ssl certificate..."

sudo certbot --nginx

# enable firewall 

echo "Enabling firewall..."

sudo ufw allow 'Nginx Full'
sudo ufw allow 'OpenSSH'
sudo ufw enable

# update

echo "Updating server..."

sudo ./update.sh

sudo systemctl enable connect

echo "Server setup complete"
