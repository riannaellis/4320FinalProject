# Use an official Python image as the base image
FROM python:3.8-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the contents of the current directory into the container
COPY . .

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Install required packages from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the Flask app will run on
EXPOSE 5000

# Command to start the Flask application
CMD ["python", "app.py"]
