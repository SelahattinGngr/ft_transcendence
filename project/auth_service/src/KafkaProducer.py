from kafka import KafkaProducer
import json
import os

def send_kafka_message(topic, data):
    producer = KafkaProducer(
        bootstrap_servers=os.getenv("KAFKA_BROKERCONNECT"),
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    producer.send(topic, data)
    producer.flush()
