# Predictive Analysis API

This project implements a RESTful API for predictive analysis in manufacturing operations using machine learning. It predicts machine downtime or production defects based on input manufacturing data.

## Features

### 1. Endpoints
- **`/upload`**:  
  Upload a CSV file containing manufacturing data.  
  **Input**: File upload (`multipart/form-data`)  
  **Example Dataset**:  
  Columns: `Machine_ID`, `Temperature`, `Run_Time`, `Downtime_Flag`  
  **cURL Example**:  
  ```bash
  curl -X POST -F "file=@data.csv" http://localhost:8000/upload
  ```
  **Success Response**:
  ```json
  {
    "message": "File uploaded successfully",
    "columns": ["Machine_ID", "Temperature", "Run_Time", "Downtime_Flag"]
  }
  ```

- **`/train`**:  
  Train a Decision Tree model on the uploaded dataset.  
  **cURL Example**:  
  ```bash
  curl -X POST http://localhost:8000/train
  ```
  **Success Response**:
  ```json
  {
    "message": "Model trained successfully",
    "accuracy": 0.9,
    "f1_score": 0.89
  }
  ```

- **`/predict`**:  
  Predict downtime using JSON input with features like `Temperature` and `Run_Time`.  
  **Input Format**:  
  ```json
  {
    "Temperature": 80,
    "Run_Time": 120
  }
  ```
  **cURL Example**:  
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"Temperature": 80, "Run_Time": 120}' http://localhost:8000/predict
  ```
  **Success Response**:
  ```json
  {
    "Downtime": "Yes",
    "Confidence": 0.85
  }
  ```
  **Error Response** (if required fields are missing):
  ```json
  {
    "error": "Missing or invalid input data"
  }
  ```

### 2. Technologies Used
- **Languages**: Python
- **Libraries**: FastAPI, pandas, scikit-learn, joblib
- **Machine Learning Model**: Decision Tree Classifier

### 3. How it Works
- **Data Upload**: Users upload a CSV file, which is stored in memory as a pandas DataFrame.
- **Training**: The model is trained on the dataset and saved for future use.
- **Prediction**: The API generates predictions using the trained model based on user inputs.

## Requirements

- Python 3.7+
- Dependencies: FastAPI, pandas, scikit-learn, joblib, uvicorn

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the API:
   ```bash
   uvicorn main:app --reload
   ```
   The API will run on `http://localhost:8000`.

4. Test the endpoints using tools like Postman or cURL.

## Example Dataset

| Machine_ID | Temperature | Run_Time | Downtime_Flag |
|------------|-------------|----------|---------------|
| 1          | 80          | 120      | 1             |
| 2          | 75          | 95       | 0             |

## Notes

- Ensure the dataset follows the specified format before uploading.
- Data cleaning and preprocessing may improve the model's performance.
- For large datasets, consider optimizing the API or using a database for storage.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
