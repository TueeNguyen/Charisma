from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import JSONResponse


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/address/{walletAddress}", response_class=JSONResponse)
async def get_data(walletAddress):
    
    json_data = {
        "message": "",
        "field": walletAddress
    }
    return JSONResponse(content=json_data)