from flask import Blueprint, request, jsonify
import pandas as pd
from .model import train_model, predict
from .utils import save_uploaded_file

main = Blueprint('main', __name__)

@main.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        filepath = save_uploaded_file(file)
        return jsonify({"message": "File uploaded successfully", "filepath": filepath}), 200

@main.route('/train', methods=['POST'])
def train():
    filepath = request.json.get('filepath')
    if not filepath:
        return jsonify({"error": "Filepath is required"}), 400
    try:
        metrics = train_model(filepath)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify(metrics), 200

@main.route('/predict', methods=['POST'])
def make_prediction():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    try:
        predictions = predict(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify(predictions), 200
