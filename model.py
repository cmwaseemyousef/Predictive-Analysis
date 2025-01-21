import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
import joblib

def train_model(file_path):
    df = pd.read_csv(file_path)
    X = df[['Temperature', 'Run_Time']]
    y = df['Downtime_Flag']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier()
    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    joblib.dump(model, 'model.pkl')
    
    return {"accuracy": accuracy, "f1_score": f1}

def predict_downtime(temperature, run_time):
    model = joblib.load('model.pkl')
    prediction = model.predict([[temperature, run_time]])
    confidence = max(model.predict_proba([[temperature, run_time]])[0])
    
    return {"Downtime": "Yes" if prediction[0] == 1 else "No", "Confidence": confidence}
