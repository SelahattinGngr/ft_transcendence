FROM debian:bullseye

RUN apt-get update && \
    apt-get install -y dos2unix curl python3 python3-pip

COPY . /app/mail_servis

RUN dos2unix /app/mail_servis/start.sh

RUN chmod +x /app/mail_servis/start.sh

RUN pip3 install -r /app/mail_servis/requirements.txt

CMD [ "/app/mail_servis/start.sh" ]
