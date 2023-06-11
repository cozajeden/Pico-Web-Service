FROM python:3.11

RUN mkdir /app
WORKDIR /app
ADD . /app/
RUN pip install -U pip && pip install -r requirements.txt