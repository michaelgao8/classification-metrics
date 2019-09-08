FROM python:3.7

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r /app/requirements.txt

RUN apt-get update

RUN apt-get install -y texlive-xetex

RUN apt-get install -y pandoc
