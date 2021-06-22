#!/bin/bash

mysql --defaults-file="$HOME/.my.piggysaving.cnf" -u piggysaving piggysaving < piggysaving_bak.sql