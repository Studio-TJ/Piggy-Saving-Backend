#!/bin/bash

# Prepare database
sudo mysql -e "CREATE DATABASE IF NOT EXISTS piggysaving"
sudo mysql -e "CREATE USER IF NOT EXISTS 'piggysaving'@'localhost' IDENTIFIED BY 'piggysaving';"
sudo mysql -e "GRANT ALL PRIVILEGES ON piggysaving.* TO 'piggysaving'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES"

sudo mysql -p piggysaving -e "CREATE TABLE piggysaving(savingDate DATE, amount FLOAT, PRIMARY KEY (savingDate))"