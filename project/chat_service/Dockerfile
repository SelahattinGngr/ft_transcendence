FROM debian:bullseye

RUN apt-get update && \
    apt-get install -y dos2unix postgresql postgresql-contrib curl python3 python3-pip libpq-dev python3-dev build-essential

COPY . /app/chat_service

COPY .conf/pg_hba.conf /etc/postgresql/13/main/pg_hba.conf

COPY .conf/postgresql.conf /etc/postgresql/13/main/postgresql.conf

RUN dos2unix /app/chat_service/start.sh

RUN dos2unix /app/chat_service/db.sh

RUN chmod +x /app/chat_service/db.sh

RUN pip3 install -r /app/chat_service/requirements.txt

RUN chmod +x /app/chat_service/start.sh

CMD [ "/app/chat_service/start.sh" ]
