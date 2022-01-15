import requests
import json
from app.config import opensea_url, opensea_key

def getWalletNFTs(walletAddress):
    url = "https://api.opensea.io/api/v1/assets"

    headers = {"Accept": "application/json"}
    params = {"owner": walletAddress}

    response = requests.request("GET", url, headers=headers, params=params)
    result = json.loads(response.text)
    return result

def getNFTData(walletAddress, contractAddress, tokenId):
    url = "https://api.opensea.io/api/v1/asset/0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb/1/"
    
    params1 = {"owner": walletAddress}
    params2 = {"contractAddress": contractAddress}
    params3 = {"tokenId": tokenId}

    response = requests.request("GET", url, params1=params1, params2=params2, params3=params3)

    print(response.text)
    return json.loads(response.text)

    #"for every item returned in above response, need to call to get floor price"
def getFloorPriceForNTF(walletAddress):
    getWalletNFTs(walletAddress=walletAddress)


    #"need to take this response and save the 7 day average floor price under stats object"
    #"take all 7 day average floor prices and sum them"
    #"this will give us the sumOfSevenDayAverage"

    #"Next Step is to get purchase price of every asset in wallet"
    #"this will give us the sumOfPurchasePrice"
    #"sumOfSevenDayAverage - sumOfPurchasePrice / sumOfPurchasePrice = performanceRate"
    #"Compare performance rate with ETH at a given time"
    return


def getCollectionsInWallet(walletAddress):
    url = "https://api.opensea.io/api/v1/collections?offset=0&limit=300"

    headers = {"Accept": "application/json"}

    params = {
        "asset_owner": walletAddress
    }

    response = requests.request("GET", url, headers=headers, params=params)

    return json.loads(response.text)