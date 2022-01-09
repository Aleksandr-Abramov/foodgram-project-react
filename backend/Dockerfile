FROM python:3.8.5

RUN mkdir /backend

COPY requirements.txt /backend

RUN pip3 install -r /backend/requirements.txt

COPY . /backend

WORKDIR /backend

CMD gunicorn foodgram_api.wsgi:application --bind 0.0.0.0:8000