FROM debian:bullseye

RUN apt-get update && \
    apt-get install -y dos2unix curl python3 python3-pip

COPY . /app/api_gateway

RUN dos2unix /app/api_gateway/start.sh

RUN chmod +x /app/api_gateway/start.sh

RUN pip3 install -r /app/api_gateway/requirements.txt

CMD [ "/app/api_gateway/start.sh" ]
