import requests
import json
from app.config import opensea_url, opensea_key

def getWalletNFTs(walletAddress):
    url = "https://api.opensea.io/api/v1/assets"

    headers = {"Accept": "application/json", "X-API-KEY": opensea_key}
    params = {
        "owner": walletAddress, 
        "limit": 50, 
        "order_direction": "asc"
    }

    response = requests.request("GET", url, headers=headers, params=params)
    #print(response.text)
    result = json.loads(response.text)
    return result

def getNFTData(walletAddress, contractAddress, tokenId):
    url = f"https://api.opensea.io/api/v1/asset/{contractAddress}/{tokenId}/"
    
    headers = {"X-API-KEY": opensea_key}

    response = requests.request("GET", url, headers=headers)

    #print(response.text)
    result = json.loads(response.text)
    return result

def getCollectionsInWallet(walletAddress):
    url = "https://api.opensea.io/api/v1/collections?offset=0&limit=300"

    headers = {"Accept": "application/json", "X-API-KEY": opensea_key}

    params = {
        "asset_owner": walletAddress
    }

    response = requests.request("GET", url, headers=headers, params=params)

    return json.loads(response.text)
