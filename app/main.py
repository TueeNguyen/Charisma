import requests
import json
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import JSONResponse

from app.etherscanAPI import getERC721Transactions

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "App is working."}


@app.get("/address/{walletAddress}", response_class=JSONResponse)
async def get_data(walletAddress):
    json_data = {
        "message": "",
        "walletAddress":walletAddress,
        "dimensions":{
            "D_or_P": getDorP(walletAddress),
            "O_or_U": getOorU(walletAddress),
            "E_or_C": getEorC(walletAddress),
            "S_or_B": getSorB(walletAddress),
        }
    }
    return JSONResponse(content=json_data)


def getDorP(walletAddress):
    walletAddress=walletAddress.lower()
    result = getERC721Transactions(walletAddress)

    sellCount = 0
    buyCount = 0
    
    for transaction in result['result']:
        if transaction['from']==walletAddress:
            sellCount+=1
        if transaction['to']==walletAddress:
            buyCount+=1

    transactionCount = buyCount + sellCount
    diamondHandMetric = sellCount / buyCount


    if diamondHandMetric < 0.3:
        value="D"
    else:
        value="P"

    userMessage = f"""We analyzed {transactionCount} ERC721 transacations on Etherscan. You had {buyCount} incoming transactions and {sellCount} outgoing transactions.
    Outgoing Transaction Count / Incoming Transaction Count = {diamondHandMetric:.2%}. If this is under 30% you're considered Diamond Hands!"""

    return {"value":value, "description": userMessage}


def getOorU(walletAddress):
    value = 'O'
    userMessage = f"""Enter text description here"""

    return {"value":value, "description": userMessage}


def getEorC(walletAddress):
    value = 'E'
    userMessage = f"""Enter text description here"""

    return {"value":value, "description": userMessage}


def getSorB(walletAddress):
    value = 'S'
    userMessage = f"""Enter text description here"""

    return {"value":value, "description": userMessage}