# pull official base image
FROM python

# set work directory
WORKDIR ../.

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt



# copy project
COPY . .


CMD uvicorn main:app --host 0.0.0.0 --port 5000