import json
import os

from kafka import KafkaConsumer

from .views import send_verification_email


def start_consumer():
    consumer = KafkaConsumer(
        'user-registration-events',
        bootstrap_servers=[os.getenv("KAFKA_BROKERCONNECT")],
        group_id='mailservice-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    for message in consumer:
        email_data = message.value
        email = email_data["email"]
        token = email_data["token"]
        # E-posta gönderme işlemini burada çağırabilirsiniz
        send_verification_email(email, token)
