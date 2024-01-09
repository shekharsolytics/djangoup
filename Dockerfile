FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y python3-pip
RUN apt-get update && apt-get install -y \
    python3  \
    gfortran musl-dev

RUN mkdir /app
WORKDIR /app

EXPOSE 8000