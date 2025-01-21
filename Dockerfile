# Use a lightweight Python image
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all project files to the working directory
COPY . .

# Install required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
