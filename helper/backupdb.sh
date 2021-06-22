#!/bin/bash

# Copy .my.piggysaving.cnf to your home directory and add it to your own crontab to enable
# auto backup

mysqldump --defaults-file="$HOME/.my.piggysaving.cnf" piggysaving > piggysaving_bak.sql