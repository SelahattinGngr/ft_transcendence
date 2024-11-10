import json
import logging
import os
import time

from kafka import KafkaConsumer

from .views import send_verification_email

logger = logging.getLogger(__name__)

def start_consumer():

    while True:
        try:
            consumer = KafkaConsumer(
                'user-registration-events',
                bootstrap_servers=[os.getenv("KAFKA_BROKERCONNECT")],
                group_id='mailservice-group',
                value_deserializer=lambda x: json.loads(x.decode('utf-8'))
            )
            logger.fatal("Connected to Kafka")
            break  # Kafka'ya bağlanıldıysa döngüden çık
        except Exception as e:
            logger.fatal(f"Failed to connect to Kafka: {e}")
            time.sleep(5)  # 5 saniye bekle ve yeniden dene

    for message in consumer:
        logger.fatal("Starting Kafka Consumer")
        logger.fatal("KAFKA_BROKERCONNECT: %s", os.getenv("KAFKA_BROKERCONNECT"))
        logger.fatal("Message: %s", message)
        logger.fatal("Message Value: %s", message.value)
        logger.fatal("consumer: %s", consumer)
        email_data = message.value
        email = email_data["email"]
        token = email_data["token"]
        # E-posta gönderme işlemini burada çağırabilirsiniz
        send_verification_email(email, token)
