FROM debian:bullseye

RUN apt-get update && \
    apt-get install -y dos2unix postgresql postgresql-contrib curl python3 python3-pip

COPY . /app/user_service

COPY .conf/pg_hba.conf /etc/postgresql/13/main/pg_hba.conf

COPY .conf/postgresql.conf /etc/postgresql/13/main/postgresql.conf

RUN dos2unix /app/user_service/start.sh

RUN dos2unix /app/user_service/db.sh

RUN chmod +x /app/user_service/db.sh

RUN pip3 install -r /app/user_service/requirements.txt

RUN chmod +x /app/user_service/start.sh

ENTRYPOINT [ "/app/user_service/db.sh" ]

CMD [ "/app/user_service/start.sh" ]