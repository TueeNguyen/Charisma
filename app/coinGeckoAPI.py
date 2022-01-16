import requests
import json

coinGecko_url = 'https://api.coingecko.com/api/v3/'


def getHistoricalEthPrice(dateString):
    url = coinGecko_url+'coins/ethereum/history'


    params = {
        'date': dateString,
    }

    headers = {"Accept": "application/json"}
    response = requests.request("GET", url, headers=headers, params=params)
    result = json.loads(response.text)
    
    return result['market_data']['current_price']['usd']