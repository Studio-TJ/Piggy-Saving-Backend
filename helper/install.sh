#!/bin/bash

BASH_DIR=`dirname $BASH_SOURCE`
BACKEND_TARGET="$HOME/.local/piggysaving"
# Install packages
sudo apt update
sudo apt install mailutils python3 python3-venv

# echo 'Enter mail address for mailing service, leave empty if you want to disable mailing service.'
# echo 'Enter the mail from address for mailing service:'
# read mailFrom
# echo 'Enter the mail to address for mailing service:'
# read mailTo

if [ -f "/etc/systemd/system/piggysaving.service" ]; then
    echo 'Disable existing service'
    sudo systemctl stop piggysaving.service
    sudo systemctl disable piggysaving.service
    sudo rm /etc/systemd/system/piggysaving.service
fi

mkdir -p $BACKEND_TARGET

python3 -m venv $BACKEND_TARGET/venv

source $BACKEND_TARGET/venv/bin/activate

pip install -r $BASH_DIR/requirements.txt

deactivate

cp -r $BASH_DIR/../backend/{restserver.py,saving.py} $BACKEND_TARGET

# sed -i 's/MAIL_FROM = ""/MAIL_FROM = "'"$mailFrom"'"/g' $BACKEND_TARGET/saving.py
# sed -i 's/MAIL_TO = ""/MAIL_TO = "'"$mailTo"'"/g' $BACKEND_TARGET/saving.py

echo 'Copy service file'
sudo cp $BASH_DIR/piggysaving.service /etc/systemd/system

echo 'Alter service file'
sudo sed -i 's/User=/User='"$USER"'/g' /etc/systemd/system/piggysaving.service
sudo sed -i 's+WorkingDirectory=+WorkingDirectory='"$HOME"'/.local/piggysaving+g' /etc/systemd/system/piggysaving.service
sudo sed -i 's+ExecStart=~+ExecStart='"$HOME"'+g' /etc/systemd/system/piggysaving.service

sudo systemctl enable piggysaving.service
sudo systemctl start piggysaving.service

# # Install frontend
# echo 'Install frontend to /var/www/piggysaving'
# sudo rm -rf /var/www/piggysaving
# pushd ../frontend/piggysaving
# npm install
# npm run build
# sudo mkdir -p /var/www/piggysaving
# sudo cp -r dist/* /var/www/piggysaving
# sudo chown -R www-data:www-data /var/www/piggysaving
# popd

echo 'Please modify your server (NGINX/Apache) settings.'