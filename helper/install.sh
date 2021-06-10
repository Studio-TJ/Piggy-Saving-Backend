#!/bin/bash

# Prepare database
sudo mysql -e "CREATE USER IF NOT EXISTS 'piggysaving'@'localhost' IDENTIFIED BY 'piggysaving';"
sudo mysql -e "GRANT ALL PRIVILEGES ON * . * TO 'piggysaving'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES"

