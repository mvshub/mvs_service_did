FROM ubuntu:16.04

COPY ./bin /server/bin
WORKDIR /server

RUN ./bin/install.sh

EXPOSE 5000

ENTRYPOINT ["./bin/didservice.py"]
