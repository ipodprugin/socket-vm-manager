FROM python:3.10-slim-bullseye

WORKDIR /backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ADD requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./database ./database
COPY ./server ./server
COPY ./*.py .
