import json
import os
from kafka import KafkaProducer

class KafkaProducerService:
    def __init__(self):
        # Kafka broker URL'sini ortam değişkenlerinden alıyoruz
        self.producer = KafkaProducer(
            bootstrap_servers=os.getenv('KAFKA_BROKER_URL'),
            value_serializer=lambda v: json.dumps(v).encode('utf-8')  # JSON serileştirici
        )

    def send_message(self, topic, message):
        """
        Belirtilen topic'e bir mesaj gönderir
        :param topic: Gönderilecek Kafka topic adı
        :param message: JSON formatında gönderilecek mesaj
        """
        try:
            self.producer.send(topic, message)
            self.producer.flush()  # Mesajı hemen gönder
            print(f"Message sent to topic {topic}: {message}")
        except Exception as e:
            print(f"Failed to send message: {e}")
