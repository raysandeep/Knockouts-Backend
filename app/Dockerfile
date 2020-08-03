# pull official base image
FROM python:3.8.3-alpine

# set work directory
WORKDIR ../.

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install psycopg2 psycopg2-binary
RUN pip install -r requirements.txt



# copy project
COPY . .