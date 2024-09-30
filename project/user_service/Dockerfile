FROM debian:bullseye

RUN apt-get update && \
    apt-get install -y dos2unix postgresql postgresql-contrib curl python3 python3-pip

COPY . /app/user_service

RUN dos2unix /app/user_service/start.sh

RUN dos2unix /app/user_service/db.sh

RUN chmod +x /app/user_service/db.sh

RUN pip3 install -r /app/user_service/requirements.txt

RUN chmod +x /app/user_service/start.sh

CMD [ "/app/user_service/start.sh" ]
