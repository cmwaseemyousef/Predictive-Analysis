from fastapi import FastAPI, File, UploadFile
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
import joblib

# Initialize the FastAPI app
app = FastAPI()

# Global variables
UPLOAD_FOLDER = "data"
MODEL_PATH = "model.pkl"

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Endpoint: Root
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Predictive Analysis API"}

# Endpoint: Upload File
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Save the uploaded file
        file_location = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_location, "wb") as f:
            f.write(await file.read())
        return {"message": "File uploaded successfully", "filepath": file_location}
    except Exception as e:
        return {"error": str(e)}

# Endpoint: Train Model
@app.post("/train")
async def train_model():
    try:
        # Load the uploaded file
        filepath = os.path.join(UPLOAD_FOLDER, "sample.csv")
        if not os.path.exists(filepath):
            return {"error": "File not found. Please upload the CSV file first."}

        # Load dataset
        data = pd.read_csv(filepath)
        X = data[["Temperature", "Run_Time"]]
        y = data["Downtime_Flag"]

        # Split dataset
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train model
        model = LogisticRegression()
        model.fit(X_train, y_train)

        # Test model
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        # Save the model
        joblib.dump(model, MODEL_PATH)

        return {"accuracy": accuracy, "f1_score": f1}
    except Exception as e:
        return {"error": str(e)}

# Endpoint: Predict
@app.post("/predict")
async def predict(data: dict):
    try:
        # Load the trained model
        if not os.path.exists(MODEL_PATH):
            return {"error": "Model not found. Please train the model first."}

        model = joblib.load(MODEL_PATH)

        # Convert input to DataFrame
        input_data = pd.DataFrame([data])

        # Make prediction
        prediction = model.predict(input_data)
        confidence = model.predict_proba(input_data).max()

        # Return prediction result
        return {"Downtime": "Yes" if prediction[0] == 1 else "No", "Confidence": confidence}
    except Exception as e:
        return {"error": str(e)}
