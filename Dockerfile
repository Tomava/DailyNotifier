FROM python:3.11-buster

RUN useradd -u 1000 scripter
RUN mkdir /home/scripter
RUN chown -R scripter /home/scripter

USER scripter
WORKDIR /home/scripter

COPY *.py ./
COPY requirements.txt ./
COPY .env ./

RUN pip3.11 install -r requirements.txt