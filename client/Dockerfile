FROM python:3.10-slim-bullseye

WORKDIR /client

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ADD requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 8080

COPY ./*.py ./
CMD ["python3", "client.py"]
