#!/usr/bin/python3

import random
import datetime
import mysql.connector as sql
from pydantic import BaseModel
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess

RANGE_MAX = 365
RATIO = 10
MAIL_TO = ""
MAIL_FROM = ""

class Saved(BaseModel):
    date: str
    saved: bool

class Withdraw(BaseModel):
    amount: float
    description: str

class RetrieveAllItem(BaseModel):
    desc: bool
    withdraw: bool

class SavingItems(BaseModel):
    date: str
    amount: str
    saved: bool

class Saving():
    def __init__(self):
        self._last = {"amount":0.0, "saved":0}
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
        if MAIL_FROM == "" or MAIL_TO == "":
            return
        db = Saving.__connectDb()
        query = "select savingDate, amount, saved, sequence from piggysaving where saved = 0 and sequence = 0"
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

    @staticmethod
    def __getNumberOfExistingEntryByDate(date: str) -> int:
        db = Saving.__connectDb()
        query = "select count(*) from piggysaving where savingDate = %s"
        value = (date,)
        db[1].execute(query, value)
        results = db[1].fetchall()
        db[0].close()
        # Retrieve how many entries already exist with the given date
        return results[0][0]

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

    @staticmethod
    def __buildSavingItems(result) -> SavingItems:
        resultRaw = {
            'date': str(result[0]),
            'amount': result[1],
            'saved': result[2]
        }
        items = SavingItems(**resultRaw)
        return items

    def retrieveAll(self, option : RetrieveAllItem):
        db = Saving.__connectDb()
        rows = dict()
        query = ""
        if option.desc:
            if not option.withdraw:
                query = "select savingDate, amount, saved from piggysaving where sequence = 0 order by savingDate desc"
            else:
                query = "select savingDate, amount, description from piggysaving where sequence <> 0 order by savingDate desc"
        else:
            if not option.withdraw:
                query = "select savingDate, amount, saved from piggysaving where sequence = 0"
            else:
                query = "select savingDate, amount, description from piggysaving where sequence <> 0"
        value = ()
        db[1].execute(query, value)
        results = db[1].fetchall()
        seq = 0
        db[0].close()
        items = []
        for result in results:
            if option.withdraw:
                rows[str(result[0]) + str(seq)] = {"date":result[0], "amount":result[1], "description":result[2]}
            else:
                rows[str(result[0]) + str(seq)] = {"date":result[0], "amount":result[1], "saved":result[2]}
                # items.append(Saving.__buildSavingItems(result))
            seq += 1
        return rows

    def sum(self):
        db = Saving.__connectDb()
        query = "select sum(amount) from piggysaving"
        value = ()
        db[1].execute(query, value)
        result = db[1].fetchone()
        sum = result[0]
        db[0].close()
        return round(sum, 2)

    def retrieveLast(self):
        db = Saving.__connectDb()
        query = "select savingDate, amount, saved from piggysaving where sequence = 0 order by savingDate desc"
        value = ()
        db[1].execute(query, value)
        result = db[1].fetchone()
        self._last['amount'] = float(result[1])
        self._last['saved'] = result[2]
        db[0].close()
        return self._last

    def updateSaved(self, item: Saved):
        db = Saving.__connectDb()
        query = "insert into piggysaving (savingDate, amount, saved, sequence) values (%s, %s, %s, %s) on duplicate key update saved=%s"
        value = (item.date, 0, True, 0, True)
        db[1].execute(query, value)
        db[0].commit()
        db[0].close()

    def withdraw(self, item: Withdraw):
        newSeq = Saving.__getNumberOfExistingEntryByDate(str(datetime.date.today()))
        db = Saving.__connectDb()
        if item.amount >= 0:
            item.amount = -item.amount
        query = "insert into piggysaving (savingDate, amount, saved, sequence, description) values (%s, %s, %s, %s, %s)"
        value = (str(datetime.date.today()), item.amount, 0, newSeq, item.description)
        db[1].execute(query, value)
        db[0].commit()
        db[0].close()

    def writeNew(self):
        numbers = self.getAmounts()
        if len(numbers) == 365:
            exit()
        last = int()
        while True:
            last = random.randrange(1, RANGE_MAX)
            last = float(last) / RATIO
            if not last in numbers:
                break

        db = Saving.__connectDb()
        query = "insert into piggysaving (savingDate, amount, saved, sequence) values (%s, %s, %s, %s) on duplicate key update amount=%s"
        value = (str(datetime.date.today()), last, False, 0, last)
        db[1].execute(query, value)
        db[0].commit()
        db[0].close()
        return last