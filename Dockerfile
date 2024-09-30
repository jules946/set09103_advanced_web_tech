# Using an official Python runtime as a parent image
FROM python:3.12-slim

# Setting working dir in container
WORKDIR /app

# Copying app source code
COPY ./src /app/src

# Copy templates and static dirs
COPY ./templates /app/templates
COPY ./static /app/static

# Copy requirements.txt and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# Exposing port for Flask app
EXPOSE 5000

# Setting environment variable for Flask
ENV FLASK_APP=/app/src/app.py

# Running Flask app
CMD ["flask", "run", "--host=0.0.0.0"]
