FROM python:3.9

WORKDIR /app

RUN apt-get -y update && apt-get install -y \
    python3.9-dev \
    apt-utils \
    python3.9-dev \
    build-essential \
    && rm -rf  /var/lib/apt/lists/*

RUN pip install --upgrade setuptools
RUN pip install \
    cython \
    numpy

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src/fastapi/ .

CMD gunicorn -w -3 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:$PORT