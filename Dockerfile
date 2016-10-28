FROM python:3.5
MAINTAINER Thiago Costa "thiagodacosta@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN make install
CMD make run
