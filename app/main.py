import requests
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import JSONResponse
import json

from app.config import etherscan_url, etherscan_key, opensea_url, opensea_key


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
            "D_or_P": getTransactions(walletAddress)
        }
    }
    return JSONResponse(content=json_data)


def getTransactions(walletAddress):
    walletAddress=walletAddress.lower()
    url = etherscan_url
    
    params = {
    'module':'account',
    'action':'tokennfttx',
    'address':walletAddress,
    'sort':'asc',
    'apikey':etherscan_key
    }

    response = requests.request("GET", url, headers={}, params=params)
    result = json.loads(response.text)

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


