#!/usr/bin/python3

import random
import datetime
import mysql.connector as sql
from pydantic import BaseModel
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess

RANGE_MAX = 365
RATIO = 10
MAIL_TO = "info@jamesvillage.dev"
MAIL_FROM= "james77676166@gmail.com"

class Item(BaseModel):
    date: str
    saved: bool
class Saving():
    def __init__(self):
        self._last = 0
        self._scheduler = BackgroundScheduler()
        self._scheduler.add_job(self.autoRoll, "cron", hour=1, minute=0)
        self._scheduler.add_job(Saving.mail, "cron", hour=22, minute=0)
        self._scheduler.start()

    @staticmethod
    def __connectDb():
        mydb = sql.connect(
            host="localhost",
            user="piggysaving",
            password="piggysaving",
            database="piggysaving"
        )
        mycursor = mydb.cursor()
        return (mydb, mycursor)

    @staticmethod
    def mail():
        db = Saving.__connectDb()
        query = "select savingDate, amount, saved from piggysaving where saved = 0"
        value = ()
        db[1].execute(query, value)
        results = db[1].fetchall()
        if (len(results) == 0) :
            return
        messageBody = "还有钱没存：\n"
        for result in results:
            messageBody += "日期：" + str(result[0]) + ", 金额：€" + str(result[1]) + "\n"
        subject = "存钱提醒"
        mailFrom = MAIL_FROM
        mailTo = MAIL_TO
        p1 = subprocess.Popen(["echo", messageBody], stdout=subprocess.PIPE)
        subprocess.call(["mail",
                         "-s",
                         subject,
                         "-r",
                         mailFrom,
                         mailTo], stdin=p1.stdout)

    def autoRoll(self):
        self.writeNew()

    def getAmounts(self):
        db = Saving.__connectDb()
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
        db = Saving.__connectDb()
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

    def retrieveLast(self):
        db = Saving.__connectDb()
        query = "select savingDate, amount from piggysaving order by savingDate desc"
        value = ()
        db[1].execute(query, value)
        result = db[1].fetchone()
        self._last = result[1]
        return self._last

    def updateSaved(self, item: Item):
        db = Saving.__connectDb()
        query = "insert into piggysaving (savingDate, amount, saved) values (%s, %s, %s) on duplicate key update saved=%s"
        value = (item.date, 0, True, True)
        db[1].execute(query, value)
        db[0].commit()
        db[0].close()

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

        db = Saving.__connectDb()
        query = "insert into piggysaving (savingDate, amount, saved) values (%s, %s, %s) on duplicate key update amount=%s"
        value = (str(datetime.date.today()), self._last, False, self._last)
        db[1].execute(query, value)
        db[0].commit()
        db[0].close()
        return self._last