from fastapi import FastAPI
import os

MODEL_DIR = os.environ.get("ML_MODEL_DIR")


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/fetch")
async def modelFetch(model_version, model_name):
    
    # moves model for deployment
    return {"1":1}

@app.get("/check")
async def versionCheck(model_version, model_name):
    
    # check if model_version and model_name are up to date
    
    return {"1":1}