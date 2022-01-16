import requests
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.responses import JSONResponse
from datetime import datetime, date

from app.etherscanAPI import getERC721Transactions, getCurrentEthPrice
from app.openseaAPI import getWalletNFTs, getNFTData, getCollectionsInWallet
from app.coinGeckoAPI import getHistoricalEthPrice
from app.config import opensea_key

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    allNFTsFromOpenSea = getWalletNFTs(walletAddress)
    allNFTsFromEtherScan = getERC721Transactions(walletAddress)
    sumOfPurchasePrice = 0
    sumOfSevenDayAverage = 0

    for asset in allNFTsFromOpenSea['assets']:
        nft = getNFTData(walletAddress, asset['asset_contract']['address'], asset['token_id'])
        sevenDayAveragePrice = nft['collection']['stats']['seven_day_average_price']
        purchasePrice = nft['collection']['payment_tokens'][0]['eth_price']
        sumOfSevenDayAverage+=sevenDayAveragePrice
        sumOfPurchasePrice+=purchasePrice
    
    performanceRate = sumOfSevenDayAverage - sumOfPurchasePrice / sumOfPurchasePrice
        
    historicalEthRate = 0
    ethPriceAtTimeOfFirstMint = 0

    for earliestNFTInWallet in allNFTsFromEtherScan['result']:
        #unformatted timestamp format example - "timeStamp":"1512907118"
        earliestNFTInWalletTimeStampUnformatted = earliestNFTInWallet['timeStamp']
        #earliestNFTInWalletTimeStamp should be in YYYY-MM-DD  
        earliestNFTInWalletTimeStamp = datetime.utcfromtimestamp(int(earliestNFTInWalletTimeStampUnformatted))
  
    currentDate = date.today()
    
    #This is an EtherScan API PRO Call, we need to replace with something else, currently using Current Price as Placeholder
    #ethPriceAtTimeOfFirstMintResponse = getHistoricalEthPrice(startDate=earliestNFTInWalletTimeStamp.date(), currentDate=currentDate)
    earliestDateString = str(earliestNFTInWalletTimeStamp.date().strftime("%d-%m-%Y"))
    ethPriceAtTimeOfFirstMintResponse = getHistoricalEthPrice(dateString = earliestDateString)
    ethPriceAtTimeOfFirstMint = float(ethPriceAtTimeOfFirstMintResponse)
    #float(ethPriceAtTimeOfFirstMintResponse['result']['ethusd'])
    
    currentEthPriceResponse = getCurrentEthPrice()
    currentEthPrice = float(currentEthPriceResponse['result']['ethusd'])

    historicalEthRate = currentEthPrice - ethPriceAtTimeOfFirstMint / ethPriceAtTimeOfFirstMint
    if performanceRate < historicalEthRate:
        performanceClassification = "Underperformed"
        value = "U"
    else:
        performanceClassification = "Overperformed"
        value = "O"  

    userMessage = \
        f"We analyzed all ERC721 transacations for this wallet and found the seven day average price of your NFT's - the purchase price / the sum of the seven " \
        f"day average has given your wallet a {performanceRate} performance rate. When compared with the historical price of ETH of the same time period you have " \
        f"been actively trading NTFs, you have {performanceClassification}"

    return {"value":value, "description": userMessage}


def getEorC(walletAddress):
    asset_owner = walletAddress
    offset=0
    limit=300

    url = f'https://api.opensea.io/api/v1/collections?asset_owner={asset_owner}&offset={offset}&limit={limit}'
    headers = {
        'Accept': 'application/json',
        'X-API-KEY': opensea_key
    }

    response = requests.request("GET", url, headers=headers)
    collections = json.loads(response.text)
    timeNow = datetime.now()

    EarlyNFTs = {}
    LaterNFTs = {}
    # looping through a list of collections from a wallet/an user
    for collection in collections: 
        created_date = datetime.strptime(collection['created_date'], "%Y-%m-%dT%H:%M:%S.%f")
        gapDays = getDateGap(getFormattedDate(created_date), getFormattedDate(timeNow))
        slug = collection['slug']
        # if the collection is minted <= 1 week -> save a key (slug of the collection) - value (the collection data) pair
        if (gapDays <= 7): 
            EarlyNFTs[slug] = collection
        else:
            LaterNFTs[slug] = collection
    # return this as a response for front-end to say something like you are E because you supported these collections early
    returned_collections = []

    if len(EarlyNFTs)/len(collections) > 0.2:
        return {'value': 'E', 'collections': EarlyNFTs}
    else: # To do: destructure into another function
        limit = 50
        offset = 0
        order_direction = 'desc'
        assets_url = f'https://api.opensea.io/api/v1/assets?owner={asset_owner}&limit={limit}&offset={offset}&order_direction={order_direction}'
        response = requests.request("GET", assets_url, headers=headers)
        assets = json.loads(response.text)['assets']
        found = False
        # Looping through all NFTs currently owned by the wallet/user
        for asset in assets: 
            asset_colllection_slug = asset['collection']['slug']
            # Check if the asset/NFT belongs to a collection in LaterNFTs
            if asset_colllection_slug in LaterNFTs and asset['last_sale']:

                asset_price = int(asset['last_sale']['total_price']) / 100000000000000000
                collection_floor_price = int(LaterNFTs[asset_colllection_slug]['stats']['floor_price'])
                # Compare the price, price bought 10% > floor_price of collection -> C type
                if(asset_price == collection_floor_price * 1.1): 
                    found = True
                    returned_collections.append(LaterNFTs[asset_colllection_slug])
        
        if found == True:
            value = 'C'
            userMessage = returned_collections
        else:
            value = 'E'
            userMessage = 'I don\'t know if you\'re E or C'

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


def getDateGap(date1, date2): 
    return (date2 - date1).days


def getFormattedDate(dateObj, format="%d/%m/%Y"): 
    return datetime.strptime(f'{dateObj.day}/{dateObj.month}/{dateObj.year}', "%d/%m/%Y")