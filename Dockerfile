FROM python:3
USER root

RUN apt-get update

ADD . .
WORKDIR .
RUN apt-get install -y vim less
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt