import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
import joblib

MODEL_PATH = 'model.pkl'

def train_model(filepath):
    data = pd.read_csv(filepath)
    X = data[['Temperature', 'Run_Time']]
    y = data['Downtime_Flag']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    return train_and_save_model(X_train, y_train, X_test, y_test)

def train_and_save_model(X_train, y_train, X_test, y_test):
    model = LogisticRegression()
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    joblib.dump(model, MODEL_PATH)
    
    return {"accuracy": accuracy, "f1_score": f1}

def predict(data):
    model = joblib.load(MODEL_PATH)
    df = pd.DataFrame([data])
    prediction = model.predict(df)
    confidence = model.predict_proba(df).max()
    
    return {"Downtime": "Yes" if prediction[0] else "No", "Confidence": confidence}
