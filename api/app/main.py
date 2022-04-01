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
from app.covalentAPI import getLastestNFTTransaction
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

@app.get("/address/getEorC/{walletAddress}", response_class=JSONResponse)
async def get_data(walletAddress):
    walletAddress=walletAddress.lower()
    result_E_or_C = getEorC(walletAddress)

    json_data = {
        "message": "",
        "walletAddress":walletAddress,
        "dimensions":{
            "E_or_C": result_E_or_C,
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
    reqCollections = getCollectionsInWallet(walletAddress) # req stands for requested
    reqNfts = getWalletNFTs(walletAddress)
    nfts = []
    collections = {}

    for reqNft in reqNfts['assets']: 
        purchasedDate = ""
        if(reqNft['last_sale'] is not None): # if OpenseaAPI last_sale is not null, cases like airdrop/mint, last_sale is null
            timestamp = reqNft['last_sale']['transaction']['timestamp']
            if(timestamp.find('.') == -1):
                timestamp += '.000000' # timestamp returned by OpenseaAPI is not consistent 
            purchasedDate = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f")
 
        else: # use CovalentAPI to find last purchased date if last_sale from OpenseaAPI is null
            SCAddress = reqNft['asset_contract']['address']
            tokenId = reqNft['token_id']
            lastestNFTTransaction =  getLastestNFTTransaction(SCAddress, tokenId)
            purchasedDate = datetime.strptime(lastestNFTTransaction, "%Y-%m-%dT%H:%M:%S%fZ")

        nfts.append({
            "name": reqNft['name'],
            "collectionSlug": reqNft['collection']['slug'],
            "purchasedDate": purchasedDate
        })      
        print(len(nfts))

    for reqCollection in reqCollections: # initialize collections
        if(reqCollection['slug'] not in collections):
            collections[reqCollection['slug']] = {
                "name": reqCollection['name'],
                "earlyNfts": [],
                "laterNfts": [],
                "createdDate": datetime.strptime(reqCollection['created_date'], "%Y-%m-%dT%H:%M:%S.%f")
            }
    
    for nft in nfts: # calculate gap days of nfts in each collection and categorize them
        slug = nft['collectionSlug']
        if(slug in collections):
            gap = getDateGap(nft['purchasedDate'], collections[slug]['createdDate'])
            if(gap <= 7): 
                collections[slug]['earlyNfts'].append(nft)
            else:
                collections[slug]['laterNfts'].append(nft)

    EMessage = ''
    CMessage = ''
    isE = False
    isC = False
    nftsCnt = len(nfts)
    for key in collections: # count the ratio between earlyNfts/laterNfts to figure out E or C
        earlyNftsCnt = len(collections[key]['earlyNfts'])
        laterNftsCnt = len(collections[key]['laterNfts'])
        name = collections[key]['name']
        if(earlyNftsCnt / nftsCnt >= 0.2):
            isE = True
            EMessage += f'{name} '
        if(laterNftsCnt / nftsCnt >= 0.2):
            isC = True
            CMessage += f'{name} '
    
    if(isE is True): 
        return {"value": "E", "description": f"You are an Early Supporter because you supported {EMessage}"}
    if(isC is True): 
        return {"value": "C", "description": f"You are an Crowd Follower because you supported {EMessage}"}

    return {"value": "X", "description": "NGMI"}

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