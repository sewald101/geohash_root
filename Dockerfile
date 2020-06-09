# FROM: https://www.codingforentrepreneurs.com/blog/django-on-docker-a-simple-introduction
# Accessed on: 06/09/2020

# Base Image
FROM python:3.7

# create and set working directory where we want to put our code
RUN mkdir /app
WORKDIR /app

# Add current directory code to working directory
ADD . /app/

# set default environment variables
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive 

# set project environment variables
# grab these via Python's os.environ
# these are 100% optional here
ENV PORT=8888

# Set DEBUG to 1 for development (1/0 vs True/False relies on tutorial settings.py above)
ENV DEBUG=0

# ENTER KEY AND SECRET KEY WHERE SHOWN
ENV AWS_ACCESS_KEY_ID=<ENTER KEY HERE>
ENV AWS_SECRET_ACCESS_KEY=<ENTER SECRET KEY HERE>

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        tzdata \
        python3-setuptools \
        python3-pip \
        python3-dev \
        python3-venv \
        git \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# install environment dependencies
RUN pip3 install --upgrade pip 
RUN pip3 install pipenv

# Install project dependencies
RUN pipenv install --skip-lock --system --dev

# These commands execute with ``Docker run``
EXPOSE 8888
CMD gunicorn geohash_proj.wsgi:application --bind 0.0.0.0:$PORT
