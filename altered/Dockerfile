FROM python:3

# prevents python buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# prevents python from writing .pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /project

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ../.. .

# remove /r from new lines if coming from windows
RUN cat django.sh | tr -d '\r'

# install system dependencies
RUN apt-get update