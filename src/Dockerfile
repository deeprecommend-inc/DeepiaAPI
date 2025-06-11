FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /code
WORKDIR /code

# Copy requirements first for better caching
COPY requirements.txt /code/

# Install Python dependencies
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /code/

CMD python3 manage.py makemigrations && python3 manage.py migrate

# ------ Ubuntsu ------

# FROM nvidia/cuda:11.5.0-cudnn8-runtime-ubuntu20.04

# # Set environment variables
# ENV PYTHON_VERSION=3.8
# ENV LANG C.UTF-8
# ENV LC_ALL C.UTF-8
# ENV TZ=Asia/Tokyo

# RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# # Install Python and pip
# RUN apt-get update && apt-get install -y python${PYTHON_VERSION} python${PYTHON_VERSION}-dev python3-pip postgresql libpq-dev

# ADD requirements.txt /

# RUN pip3 install --upgrade pip

# RUN pip3 install -r requirements.txt

# # Clean up APT when done.
# RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# # Set the working directory

# WORKDIR /code


# ADD . /code/

# CMD python3 manage.py makemigrations && python3 manage.py migrate
