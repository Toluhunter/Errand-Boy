FROM python:3.10.3-slim-bullseye

# copy code to docker

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# Setup dependecies for python and cmake

RUN apt-get -y update
RUN apt-get install -y --fix-missing \
    build-essential \
    cmake \
    git \
    pkg-config \
    python3-dev \
    software-properties-common \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*

# Setup project dependencies

COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN cd / && \
    mkdir -p dlib && \
    git clone -b 'v19.9' --single-branch https://github.com/davisking/dlib.git dlib/ && \
    cd  dlib/ && \
    python3 setup.py install --yes USE_AVX_INSTRUCTIONS

RUN pip install face-recognition

WORKDIR /app
RUN cd /app
COPY . .

#  create gunicorn log directory
RUN mkdir /var/log/gunicorn

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  


EXPOSE 8000 

CMD ["gunicorn", "-c", "config/gunicorn/gunicorn.conf.py"]