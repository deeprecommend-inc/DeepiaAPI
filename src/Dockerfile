FROM python:3.9

ENV PYTHONUNBUFFERED 1

RUN mkdir /code

WORKDIR /code

ADD requirements.txt /code/

RUN pip3 cache purge

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

ADD . /code/

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
