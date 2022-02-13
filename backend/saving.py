#!/usr/bin/python3

import random
import datetime
from sre_constants import RANGE
import sqlite3
from pydantic import BaseModel
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess

RANGE_MAX = 365
RATIO = 10
DB_FILENAME = "piggysaving.db"
DB_VERSION = 1
MAIL_TO = ""
MAIL_FROM = ""

class Saved(BaseModel):
    date: str
    saved: bool

class Withdraw(BaseModel):
    amount: float
    description: str

class Invest(BaseModel):
    amount: float
    description: str
class RetrieveAllItem(BaseModel):
    desc: bool
    withdraw: bool

class SavingItems(BaseModel):
    date: str
    amount: str
    saved: bool

def dbMigration(con: sqlite3.Connection, cur: sqlite3.Cursor):
    cur.execute("select * from version")
    currentVersion = cur.fetchone()[0]
    if currentVersion == DB_VERSION:
        print("Running db version", str(DB_VERSION), ", no migration needed.")
    else:
        print("Migration needed from version", str(currentVersion), "to", str(DB_VERSION))
        # current no migration has happened..

def initializeDb():
    con = sqlite3.connect(DB_FILENAME)
    cur = con.cursor()
    cur.execute(
        "create table if not exists piggysaving(\
            amount real,\
            date text,\
            saved int,\
            sequence int,\
            description text,\
            type text,\
            primary key (date, sequence))"
    )
    cur.execute("create table if not exists version(versionNumber int, primary key (versionNumber))")
    cur.execute("insert or ignore into version (versionNumber) values (?)", (DB_VERSION, ))
    con.commit()
    dbMigration(con, cur)
    con.close()

class Saving():
    def __init__(self):
        initializeDb()
        self._last = {"amount":0.0, "saved":0}
        self._scheduler = BackgroundScheduler()
        self._scheduler.add_job(self.autoRoll, "cron", hour=1, minute=0)
        # self._scheduler.add_job(Saving.mail, "cron", hour=22, minute=0)
        self._scheduler.start()

    @staticmethod
    def __connectDb():
        con = sqlite3.connect(DB_FILENAME)
        cur = con.cursor()
        return (con, cur)

    @staticmethod
    def mail():
        if MAIL_FROM == "" or MAIL_TO == "":
            return
        db = Saving.__connectDb()
        query = "select savingDate, amount, saved, type from piggysaving where saved = 0 and type = 'saving'"
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
        db[0].close()

    @staticmethod
    def __getNumberOfExistingEntryByDate(date: str) -> int:
        db = Saving.__connectDb()
        db[1].execute("select count(*) from piggysaving where date = ?", (date,))
        results = db[1].fetchone()
        db[0].close()
        # Retrieve how many entries already exist with the given date
        if results[0] == 0:
            return 1
        else:
            return results[0]

    def autoRoll(self):
        self.writeNew()

    def getAmounts(self):
        db = Saving.__connectDb()
        db[1].execute("select amount from piggysaving where amount > 0 order by date desc")
        results = db[1].fetchall()
        numbers = []
        for result in results:
            numbers.append(result[0])
        db[0].close()
        numCycle = int(len(numbers) / 365)
        numbers = numbers[:(len(numbers) - numCycle * RANGE_MAX)]
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
        if not option.withdraw:
            db[1].execute("select date, amount, saved, description, type from piggysaving where type = 'saving' order by date desc")
        else:
            db[1].execute("select date, amount, saved, description, type from piggysaving where type = 'cost' order by date desc")
        results = db[1].fetchall()
        seq = 0
        db[0].close()

        for result in results:
            rows[result[0] + str(seq)] = {"date":result[0], "amount":result[1], "saved":result[2], "description":result[3], "type":result[4]}
                # items.append(Saving.__buildSavingItems(result))
            seq += 1
        return rows

    def sum(self):
        db = Saving.__connectDb()
        db[1].execute("select sum(amount) from piggysaving where saved = 1")
        result = db[1].fetchone()
        sum = 0
        if result[0] is  not None:
            sum = result[0]
        db[0].close()
        return round(sum, 2)

    def sumAll(self):
        db = Saving.__connectDb()
        db[1].execute("select sum(amount) from piggysaving where type = 'saving'")
        result = db[1].fetchone()
        sum = 0
        if result[0] is  not None:
            sum = result[0]
        db[0].close()
        return round(sum, 2)

    def sumInvested(self):
        db = Saving.__connectDb()
        db[1].execute("select sum(amount) from piggysaving where type ='invest'")
        result = db[1].fetchone()
        sum = 0
        if result[0] is not None:
            sum = -result[0]
        db[0].close()
        return round(sum, 2)

    def used(self):
        db = Saving.__connectDb()
        db[1].execute("select sum(amount) from piggysaving where type = 'cost'")
        result = db[1].fetchone()
        sum = 0
        if result[0] is not None:
            sum = -result[0]
        db[0].close()
        return round(sum, 2)

    def retrieveLast(self):
        db = Saving.__connectDb()
        db[1].execute("select date, amount, saved from piggysaving where type = 'saving' order by date desc")
        result = db[1].fetchone()
        if result is not None:
            self._last['amount'] = float(result[1])
            self._last['saved'] = result[2]
        db[0].close()
        return self._last

    def updateSaved(self, item: Saved):
        db = Saving.__connectDb()
        db[1].execute("update piggysaving set saved = ? where date = ? and sequence = 0", (int(item.saved), item.date))
        db[0].commit()
        db[0].close()

    def withdraw(self, item: Withdraw):
        newSeq = Saving.__getNumberOfExistingEntryByDate(str(datetime.date.today()))
        db = Saving.__connectDb()
        if item.amount >= 0:
            item.amount = -item.amount
        db[1].execute("insert or ignore into piggysaving (date, amount, saved, sequence, description, type) values (?, ?, ?, ?, ?, ?)", (str(datetime.date.today()), item.amount, 1, newSeq, item.description, 'cost'))
        db[0].commit()
        db[0].close()

    def invest(self, item: Invest):
        newSeq = Saving.__getNumberOfExistingEntryByDate(str(datetime.date.today()))
        db = Saving.__connectDb()
        if item.amount >= 0:
            item.amount = -item.amount
        db[1].execute("insert or ignore into piggysaving (date, amount, saved, sequence, description, type) values (?, ?, ?, ?, ?, ?)", (str(datetime.date.today()), item.amount, 1, newSeq, item.description, 'invest'))
        db[0].commit()
        db[0].close()

    def invested(self):
        db = Saving.__connectDb()
        rows = dict()
        db[1].execute("select date, amount, description from piggysaving where type = 'invest' order by date desc")
        results = db[1].fetchall()
        db[0].close()
        for result in results:
            rows[str(result[0])] = {"date":result[0], "amount":result[1], "description":result[2]}

        return rows

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
        db[1].execute("insert or ignore into piggysaving (date, amount, saved, sequence, description, type) values (?, ?, ?, ?, ?, ?)", (str(datetime.date.today()), last, 0, 0, None, 'saving'))
        db[0].commit()
        db[0].close()
        return last