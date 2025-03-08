FROM python:3.10-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV TZ=Europe/Moscow
ENV SUMO_HOME=/usr/share/sumo

RUN apt update && apt install -y git g++ gcc && apt install -y sumo

COPY requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt

COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

RUN apt-get update && apt-get install nano
COPY /src /app
ENTRYPOINT [ "/usr/local/bin/entrypoint.sh" ]
