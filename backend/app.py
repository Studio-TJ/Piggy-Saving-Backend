#!/usr/bin/python3

import os
import random
import csv
import datetime

RANGE_MAX = 365
WORKINGDIR = os.path.dirname(os.path.realpath(__file__))
FILE = WORKINGDIR + "/tmp/tmp.csv"


if not os.path.exists(WORKINGDIR + "/tmp"):
    os.mkdir(WORKINGDIR + "/tmp")

def retrieveExisting():
    numbers = set()
    if os.path.exists(FILE):
        rows = dict()
        with open(FILE, 'r') as csvFile:
            reader = csv.reader(csvFile, delimiter=' ', quotechar='|')
            for row in reader:
                rows[row[0]] = row[1]
                numbers.add(int(float(row[1])*10))
            if str(datetime.date.today()) in rows:
                del rows[str(datetime.date.today())]

        with open(FILE, 'w')  as csvFile:
            writer = csv.writer(csvFile, delimiter=' ')
            for key in rows:
                writer.writerow([key, rows[key]])

    return numbers

def main():
    numbers = retrieveExisting()
    if len(numbers) == 365:
        exit()
    currentNum = int()
    while True:
        currentNum = random.randrange(1, RANGE_MAX)
        if not currentNum in numbers:
            break
    if os.path.exists(FILE):
        mode = 'a'
    else:
        mode = 'w'
    with open(FILE, mode) as csvFile:
        writer = csv.writer(csvFile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([datetime.date.today(), str(float(currentNum)/10)])

if __name__ == "__main__":
    main()