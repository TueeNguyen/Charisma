# Charisma-API
This is the backend for the Charisma web application. It was built as part of NFTHack 2022.

## How it works:
1. Request is sent to primary /address/{walletAddress} endpoint.

2. Data is aggregated from several APIs
- OpenSea API (primary)
- etherScan API
- CoinGeckoAPI

3. Results are processed according to the Wallet Personality Indicator (WPI) definitions.

4. A response is returned with the 4 key dimensions of the WPI.

## Instructions to Run Locally
1. setup and activate python venv (python version 3.7.3)
2. install requirements.txt
3. If running locally, put your api keys into "config.py" and comment out os.environ[] line
4. At project root, execute: uvicorn app.main:app --reload
5. You'll then be able to view: http://127.0.0.1:8000 and http://127.0.0.1:8000/docs for API documentation.

## Deployment Instructions
1. Build Docker Image
```docker build -t charisma-api . ```

2. Tag Image
```docker tag charisma-api {dockerhub username}/charisma-api ```

3. Push to container registry
```docker push {dockerhub username}/charisma-api```

4. Deploy Container on Hosting Service (e.g Azure App Service).
(PLease ensure to set API Keys listed in app/config.py as environment variables)

## Our Deployment
We have deployed API on Microsoft Azure using AppService.
Docs: https://charisma-api.azurewebsites.net/docs
API URL: https://charisma-api.azurewebsites.net/


## Outstanding Items
- improved error handling must be implemented
- further testing of determination indicator logic

## Possible Improvements
- Look at implementing more advanced indicator determination logic (e.g. possible data science / machine learning)
- Look at other indicators!