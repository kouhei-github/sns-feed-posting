# Dockerfile

# Pull the Python 3.12 image from Docker Hub
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY ./container/requirements.txt /tmp

# Install any requirements (libraries, frameworks, etc.)
RUN pip install -r /tmp/requirements.txt

# Copy the rest of your application's code into the container
COPY ./src /app

# Run your application
#CMD ["python", "./main.py"]