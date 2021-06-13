#!/usr/bin/python3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from saving import Saving
from saving import Item

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

@app.get("/roll")
async def roll():
    num = sav.writeNew()
    return {"newNum": float(num)}

@app.get("/all")
async def getAll():
    return sav.retrieveAll()

@app.get("/sum")
async def getSum():
    return {"sum": sav.sum()}

@app.get("/last")
async def getLast():
    return {"last": sav.retrieveLast()}

@app.post("/save")
async def updateSaved(item: Item):
    return sav.updateSaved(item)