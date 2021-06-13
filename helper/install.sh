#!/bin/bash

# Install packages
# sudo apt update
# sudo apt install mailutils mariadb

# Prepare database
# sudo mysql -e "CREATE DATABASE IF NOT EXISTS piggysaving"
# sudo mysql -e "CREATE USER IF NOT EXISTS 'piggysaving'@'localhost' IDENTIFIED BY 'piggysaving';"
# sudo mysql -e "GRANT ALL PRIVILEGES ON piggysaving.* TO 'piggysaving'@'localhost';"
# sudo mysql -e "FLUSH PRIVILEGES"

# sudo mysql -p piggysaving -e "CREATE TABLE piggysaving(savingDate DATE, amount FLOAT, saved BOOLEAN, PRIMARY KEY (savingDate))"


echo 'Enter mail address for mailing service, leave empty if you want to disable mailing service.'
echo 'Enter the mail from address for mailing service:'
read mailFrom
echo 'Enter the mail to address for mailing service:'
read mailTo

if [ -f "/etc/systemd/system/piggysaving.service" ]; then
    echo 'Disable existing service'
    sudo systemctl stop piggysaving.service
    sudo systemctl disable piggysaving.service
    sudo rm /etc/systemd/system/piggysaving.service
fi

mkdir -p $HOME/.local/piggysaving

cp -r ../backend/{restserver.py,saving.py} $HOME/.local/piggysaving

sed -i 's/MAIL_FROM = ""/MAIL_FROM = "'"$mailFrom"'"/g' $HOME/.local/piggysaving/saving.py
sed -i 's/MAIL_TO = ""/MAIL_TO = "'"$mailTo"'"/g' $HOME/.local/piggysaving/saving.py

echo 'Copy service file'
sudo cp piggysaving.service /etc/systemd/system

echo 'Alter service file'
sudo sed -i 's/User=/User='"$USER"'/g' /etc/systemd/system/piggysaving.service
sudo sed -i 's+WorkingDirectory=+WorkingDirectory='"$HOME"'/.local/piggysaving+g' /etc/systemd/system/piggysaving.service

sudo systemctl enable piggysaving.service
sudo systemctl start piggysaving.service
