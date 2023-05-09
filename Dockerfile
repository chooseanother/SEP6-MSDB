# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /msdb
COPY requirements.txt /msdb/
RUN pip install -r requirements.txt
COPY . /msdb/
