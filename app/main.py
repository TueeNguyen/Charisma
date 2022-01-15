import requests
import json
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import JSONResponse

from app.etherscanAPI import getERC721Transactions
from app.openseaAPI import getWalletNFTs, getNFTData, getFloorPriceForNTF, getCollectionsInWallet


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "App is working."}


@app.get("/address/{walletAddress}", response_class=JSONResponse)
async def get_data(walletAddress):
    walletAddress=walletAddress.lower()

    result_D_or_P = getDorP(walletAddress)
    result_O_or_U = getOorU(walletAddress)
    result_E_or_C = getEorC(walletAddress)
    result_S_or_B = getSorB(walletAddress)

    json_data = {
        "message": "",
        "walletAddress":walletAddress,
        "dimensions":{
            "D_or_P": result_D_or_P,
            "O_or_U": result_O_or_U,
            "E_or_C": result_E_or_C,
            "S_or_B": result_S_or_B,
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
    
    if buyCount > 0:
        diamondHandMetric = sellCount / buyCount
        if diamondHandMetric < 0.3:
            value="D"
        else:
            value="P"

        userMessage = \
        f"We analyzed {transactionCount} ERC721 transacations on Etherscan. " \
        f"You had {buyCount} incoming transaction(s) and {sellCount} outgoing transaction(s). " \
        f"Outgoing Transaction Count / Incoming Transaction Count = {diamondHandMetric:.0%}. " \
        f"If this is under 30% you're considered Diamond Hands! "    
    else:
        diamondHandMetric = 0
        value="X"
        userMessage = "No NFTs in provided address."    

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
    cutoff = 2000
    mixCutoff = 0.3
    result = getCollectionsInWallet(walletAddress)

    blueChipCount = 0
    smallProjectCount = 0
    
    for collection in result:
        if collection['stats']['total_volume'] > cutoff:
            collectionType='Bluechip'
            blueChipCount+=1
        else:
            collectionType='Small Project'
            smallProjectCount+=1

        #print(collection['name'],'- Total Volume',collection['stats']['total_volume'], collectionType)
        #print(blueChipCount,smallProjectCount)

    totalProjectCount = blueChipCount + smallProjectCount

    if totalProjectCount > 0:
        smallProjectMix = smallProjectCount / totalProjectCount
        
        if smallProjectMix > mixCutoff:
            value="S"
        else:
            value="B"
        
        userMessage = \
        f"Based on Opensea, you are currently particpating in {smallProjectCount} " \
        f"small projects with total transaction volume < 2,000 ETH. " \
        f"You are participating in {totalProjectCount} total projects. " \
        f"Small Project mix: {smallProjectMix:.0%}. > 50% small project mix is required " \
        f"to be a small project supporter."

    else:
        smallProjectMix = 0
        value = "X"
        userMessage = "No NFTs in provided address."    

    return {"value":value, "description": userMessage}