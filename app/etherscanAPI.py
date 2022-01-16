import requests
import json
from app.config import etherscan_url, etherscan_key

def getERC721Transactions(walletAddress):
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
    return result


def getHistoricalEthPrice(startDate, currentDate):
    url = etherscan_url
    
    params = {
    'module':'stats',
    'action':'ethdailyprice',
    'startdate':startDate,
    'enddate':currentDate,
    'sort':'asc',
    'apikey':etherscan_key
    }

    response = requests.request("GET", url, headers={}, params=params)
    result = json.loads(response.text)
    return result


def getCurrentEthPrice():
    url = etherscan_url
    
    params = {
    'module':'stats',
    'action':'ethprice',
    'apikey':etherscan_key
    }

    response = requests.request("GET", url, headers={}, params=params)
    result = json.loads(response.text)
    return result