FROM python:slim-buster

WORKDIR /app

COPY requirements.txt /app/

RUN python3 -m pip install -r requirements.txt

COPY script.sh /app/

COPY . /app/