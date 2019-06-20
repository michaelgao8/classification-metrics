FROM python:3.7

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r /app/requirements.txt
