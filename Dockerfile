# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# IMPORTANT: Set GOOGLE_API_KEY as an environment variable
# when running the container, or use Google Cloud Secret Manager.
# Example: docker run -e GOOGLE_API_KEY="your_actual_api_key" your_image_name
# ENV GOOGLE_API_KEY YOUR_GOOGLE_API_KEY_HERE

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# Using --no-cache-dir to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
# Ensure chat_logic.py is in the root of your project directory
COPY main.py .
COPY chat_logic.py .
COPY static/ ./static/

# Expose port 8080, as expected by Cloud Run by default
EXPOSE 8080

# Define the command to run the application, explicitly using port 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"] 