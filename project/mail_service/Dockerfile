FROM debian:bullseye

RUN apt-get update && \
    apt-get install -y dos2unix curl python3 python3-pip

COPY . /app/mail_service

RUN dos2unix /app/mail_service/start.sh

RUN chmod +x /app/mail_service/start.sh

RUN pip3 install -r /app/mail_service/requirements.txt

ENTRYPOINT [ "/app/mail_service/start.sh" ]
