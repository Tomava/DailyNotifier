FROM python:3.14

RUN useradd -u 1000 scripter
RUN mkdir /home/scripter
RUN chown -R scripter /home/scripter

USER scripter
WORKDIR /home/scripter

COPY *.py ./
COPY requirements.txt ./
COPY .env ./

RUN pip3.14 install -r requirements.txt
