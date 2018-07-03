FROM ubuntu:16.04

RUN apt-get update -y
RUN apt-get install -y apt-utils net-tools curl wget
RUN apt-get install -y python3-pip python3.5
RUN apt-get install -y sqlite3

RUN pip3 install flask flask-sqlalchemy sqlalchemy-utils

RUN apt-get autoremove && apt-get clean

COPY . /server
WORKDIR /server

EXPOSE 5000

ENTRYPOINT ["python3.5", "didservice.py"]
