#!/usr/bin/python3

import os
import random
import csv
import datetime
import mysql.connector as sql

RANGE_MAX = 365
RATIO = 10
class Saving():
    def __init__(self):
        self._last = 0

    def __connectDb(self):
        mydb = sql.connect(
            host="localhost",
            user="piggysaving",
            password="piggysaving",
            database="piggysaving"
        )
        mycursor = mydb.cursor()
        return (mydb, mycursor)

    def getAmounts(self):
        db = self.__connectDb()
        query = "select amount from piggysaving"
        value = ()
        db[1].execute(query, value)
        results = db[1].fetchall()
        numbers = set()
        for result in results:
            numbers.add(result[0])
        db[0].close()
        return numbers

    def retrieveAll(self):
        db = self.__connectDb()
        rows = dict()
        query = "select savingDate, amount, saved from piggysaving"
        value = ()
        db[1].execute(query, value)
        results = db[1].fetchall()
        for result in results:
            rows[result[0]] = {"date":result[0], "amount":result[1], "saved":result[2]}

        db[0].close()
        return rows

    def sum(self):
        sum = 0
        allAmounts = self.getAmounts()
        for num in allAmounts:
            sum += num
        return round(sum, 2)

    def getLast(self):
        return self._last

    def writeNew(self):
        numbers = self.getAmounts()
        if len(numbers) == 365:
            exit()
        self._last = int()
        while True:
            self._last = random.randrange(1, RANGE_MAX)
            self._last = float(self._last) / RATIO
            if not self._last in numbers:
                break

        db = self.__connectDb()
        query = "insert into piggysaving (savingDate, amount, saved) values (%s, %s, %s) on duplicate key update amount=%s"
        value = (str(datetime.date.today()), self._last, False, self._last)
        db[1].execute(query, value)
        db[0].commit()
        db[0].close()
        return self._last