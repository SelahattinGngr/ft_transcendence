import json
import logging
import os
from kafka import KafkaProducer

logger = logging.getLogger(__name__)

def send_message(topic, data):
    logger.fatal("Sending Kafka Message")
    logger.fatal("KAFKA_BROKERCONNECT: %s", os.getenv("KAFKA_BROKERCONNECT"))

    producer = KafkaProducer(
        bootstrap_servers=os.getenv("KAFKA_BROKERCONNECT"),
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    producer.send(topic, data)
    producer.flush()
