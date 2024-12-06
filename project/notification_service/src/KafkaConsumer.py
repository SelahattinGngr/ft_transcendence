import json
import logging
import os
import time

from .views import notification_type_request

from kafka import KafkaConsumer

logger = logging.getLogger(__name__)

def start_consumer():
    while True:
        try:
            consumer = KafkaConsumer(
                'user-notification-events',
                bootstrap_servers=[os.getenv("KAFKA_BROKERCONNECT")],
                group_id='mailservice-group',
                value_deserializer=lambda x: json.loads(x.decode('utf-8'))
            )
            logger.fatal("Connected to Kafka")
            break
        except Exception as e:
            logger.fatal(f"Failed to connect to Kafka: {e}")
            time.sleep(5)

    for message in consumer:
        logger.fatal("Starting Kafka Consumer")
        logger.fatal("KAFKA_BROKERCONNECT: %s", os.getenv("KAFKA_BROKERCONNECT"))
        logger.fatal("Message: %s", message)
        logger.fatal("Message Value: %s", message.value)
        logger.fatal("consumer: %s", consumer)
        if (message.topic == "user-notification-events"):
            data = message.value
            user_name = data["username"]
            type = data["type"]
            content = data["content"]
            notification_type_request(user_name, type, content)

