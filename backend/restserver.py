#!/usr/bin/python3
from typing import Optional

from fastapi import FastAPI
# import .saving
from saving import Saving

app = FastAPI()

# sav = saving.Saving()
sav = Saving()

@app.get("/roll")
def roll():
    num = sav.writeNew()
    return {"newNum": float(num)/10}

@app.get("/all")
def getAll():
    return sav.retrieveAll()

@app.get("/sum")
def getSum():
    return {"sum": sav.sum()}