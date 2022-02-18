#!/usr/bin/python3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from saving import Saving
from saving import Saved, RetrieveAllItem, Withdraw, Invest, Config, Roll

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8880",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# sav = saving.Saving()
sav = Saving()

@app.post("/roll")
async def roll(item: Roll):
    num = sav.writeNew(item)
    return {"newNum": float(num)}

@app.post("/all")
async def getAll(item: RetrieveAllItem):
    return sav.retrieveAll(item)

@app.get("/sum")
async def getSum():
    return {"sum": sav.sum()}

@app.get("/sumAll")
async def getSum():
    return {"sumAll": sav.sumAll()}

@app.get("/sumInvested")
async def getSumInvested():
    return {"sumInvested": sav.sumInvested()}

@app.get("/used")
async def getSum():
    return {"used": sav.used()}

@app.get("/last")
async def getLast():
    return {"last": sav.retrieveLast()}

@app.post("/save")
async def updateSaved(item: Saved):
    return sav.updateSaved(item)

@app.post("/withdraw")
async def withdraw(item: Withdraw):
    return sav.withdraw(item)

@app.post("/invest")
async def invest(item: Invest):
    return sav.invest(item)

@app.get("/invested")
async def invested():
    return sav.invested()

@app.post("/updateconfig")
async def updateConfig(item: Config):
    return sav.updateConfig(item)