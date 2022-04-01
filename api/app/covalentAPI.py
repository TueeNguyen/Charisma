import requests
import json




def getLastestNFTTransaction(contractAddress, tokenId):
    covalentUrl = f'https://api.covalenthq.com/v1/1/tokens/{contractAddress}/nft_transactions/{tokenId}/?quote-currency=USD&format=JSON&key=ckey_docs'

    response = requests.request("GET", covalentUrl)

    result = json.loads(response.text)
    return result['data']['items'][0]['nft_transactions'][0]['block_signed_at']