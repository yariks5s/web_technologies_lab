FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
#RUN apt-get update && apt-get install -y \
#    libmysqlclient-dev

# Set working directory
WORKDIR /

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port that the app will listen on
EXPOSE 8000 

