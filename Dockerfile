FROM python:3.8

ARG RAILWAY_ENVIRONMENT
ENV RAILWAY_ENVIRONMENT=$RAILWAY_ENVIRONMENT

# Update package lists
RUN apt-get update

# Install required packages
RUN apt-get install -y ffmpeg libsm6 libxext6

# Set working directory
WORKDIR /app

# Copy your application code into the container
COPY . /app

# Install application dependencies

RUN PYTHONPATH=/usr/bin/python pip install -r requirements.txt

# Set the command to run your application
CMD [ "python", "main.py" ]
