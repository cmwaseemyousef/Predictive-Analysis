from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import pandas as pd
import os
from model import train_model, predict_downtime

app = FastAPI()

class PredictionInput(BaseModel):
    Temperature: float
    Run_Time: float

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        os.makedirs('data', exist_ok=True)
        df.to_csv('data/manufacturing_data.csv', index=False)
        df.to_csv('data/manufacturing_data.csv', index=False)
        return {"message": "File uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing file: {e}")

@app.post("/train")
async def train():
    try:
        metrics = train_model('data/manufacturing_data.csv')
        return metrics
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Training data not found. Please upload the data file first.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during training: {e}")

@app.post("/predict")
async def predict(input: PredictionInput):
    try:
        prediction = predict_downtime(input.Temperature, input.Run_Time)
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during prediction: {e}")