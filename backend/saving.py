#!/usr/bin/python3

import os
import random
import csv
import datetime
import mysql.connector as sql

RANGE_MAX = 365
class Saving():
    def __init__(self):
        self._mydb = sql.connect(
            host="localhost",
            user="piggysaving",
            password="piggysaving",
            database="piggysaving"
        )
        self._mycursor = self._mydb.cursor()

    def getAmounts(self):
        query = "select amount from piggysaving"
        value = ()
        self._mycursor.execute(query, value)
        results = self._mycursor.fetchall()
        numbers = set()
        for result in results:
            numbers.add(result[0])
        return numbers

    def retrieveAll(self):
        rows = dict()
        query = "select savingDate, amount from piggysaving"
        value = ()
        self._mycursor.execute(query, value)
        results = self._mycursor.fetchall()
        for result in results:
            rows[result[0]] = result[1]
        return rows

    def sum(self):
        sum = 0
        allAmounts = self.getAmounts()
        for num in allAmounts:
            sum += num
        return sum

    def writeNew(self):
        numbers = self.getAmounts()
        if len(numbers) == 365:
            exit()
        currentNum = int()
        while True:
            currentNum = random.randrange(1, RANGE_MAX)
            currentNumReal = float(currentNum) / 10
            if not currentNumReal in numbers:
                break

        query = "insert into piggysaving (savingDate, amount) values (%s, %s) on duplicate key update amount=%s"
        value = (str(datetime.date.today()), currentNumReal, currentNumReal)
        self._mycursor.execute(query, value)
        self._mydb.commit()

        return currentNum