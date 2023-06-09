FROM python:3.8.15-bullseye
RUN pip install --user --upgrade pip
RUN apt-get update
RUN apt-get -y install unixodbc-dev
COPY . ./tmp/data_preparation
RUN bash ./tmp/data_preparation/msodbcsql17.sh
RUN pip install ./tmp/data_preparation