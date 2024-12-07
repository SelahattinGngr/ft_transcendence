FROM debian:bullseye

RUN apt-get update && \
    apt-get install -y dos2unix postgresql postgresql-contrib curl python3 python3-pip

COPY . /app/log_service

COPY .conf/pg_hba.conf /etc/postgresql/13/main/pg_hba.conf

COPY .conf/postgresql.conf /etc/postgresql/13/main/postgresql.conf

RUN dos2unix /app/log_service/start.sh

RUN dos2unix /app/log_service/db.sh

RUN chmod +x /app/log_service/db.sh

RUN pip3 install -r /app/log_service/requirements.txt

RUN chmod +x /app/log_service/start.sh

ENTRYPOINT [ "/app/log_service/db.sh" ]

CMD [ "/app/log_service/start.sh" ]