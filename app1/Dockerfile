# pull official base image
FROM python:3.8.3-alpine

# set work directory
WORKDIR ../.

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apk add build-base
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt



# copy project
COPY . .