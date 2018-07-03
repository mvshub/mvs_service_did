FROM ubuntu:latest

RUN apt-get update -y
RUN apt-get install -y python3-pip python3.5
RUN apt-get install -y sqlite3 libsqlite3-dev

COPY . /server
WORKDIR /server

RUN pip3 install flask flask-sqlalchemy sqlalchemy-utils

ENTRYPOINT ["python3.5"]
CMD ["didservice.py"]