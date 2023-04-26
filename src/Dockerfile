# pull official base image
FROM python:slim

## set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt update
RUN apt upgrade
RUN apt -y install netcat gcc
RUN apt clean

# copy requirements file
COPY ./requirements.txt /usr/src/app/

# install python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy project
COPY ./ /usr/src/app/
