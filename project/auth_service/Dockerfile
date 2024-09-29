FROM debian:bullseye

RUN apt-get update && \
    apt-get install -y dos2unix postgresql postgresql-contrib curl python3 python3-pip

COPY . /app/auth_service

RUN dos2unix /app/auth_service/start.sh

RUN dos2unix /app/auth_service/db.sh

RUN chmod +x /app/auth_service/db.sh

RUN pip3 install -r /app/auth_service/requirements.txt

RUN chmod +x /app/auth_service/start.sh

CMD [ "/app/auth_service/start.sh" ]
