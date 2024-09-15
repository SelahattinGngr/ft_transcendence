FROM debian:bullseye

RUN apt-get update && \
    apt-get install -y postgresql postgresql-contrib curl python3 python3-pip

COPY . /app/auth_service
RUN chmod +x /app/auth_service/db.sh

RUN pip3 install -r /app/auth_service/requirements.txt

RUN chmod +x /app/auth_service/start.sh

CMD [ "/app/auth_service/start.sh" ]