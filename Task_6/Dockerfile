FROM python:3.7-slim-buster

COPY . /app
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 1

RUN pip install --upgrade pip

# prerequisites
RUN pip install -U nltk

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt 
# making directory of app
WORKDIR /app
# copying all files over
COPY . .

# expose port 8000
EXPOSE 8080

CMD gunicorn -w 4 -b:8080  app:app --preload --timeout 400
