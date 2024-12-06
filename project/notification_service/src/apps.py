from django.apps import AppConfig
from django.conf import settings
import threading
import logging

class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src'

    def ready(self):
        try:
            # Kafka consumer'ı bir thread içinde başlatıyoruz
            kafka_thread = threading.Thread(target=self.start_kafka_consumer, daemon=True)
            kafka_thread.start()
            # Thread başlatıldıktan sonra çalışmaya devam ediyoruz
            logging.info("Kafka Consumer thread başlatıldı.")
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(f"Kafka consumer başlatılırken hata oluştu: {e}")

    # def ready(self):
    #     if getattr(settings, 'ENABLE_KAFKA', False):
    #         try:
    #             # Kafka consumer'ı bir thread içinde başlatıyoruz
    #             kafka_thread = threading.Thread(target=self.start_kafka_consumer, daemon=True)
    #             kafka_thread.start()
    #             # Thread başlatıldıktan sonra çalışmaya devam ediyoruz
    #             logging.info("Kafka Consumer thread başlatıldı.")
    #         except Exception as e:
    #             logger = logging.getLogger(__name__)
    #             logger.error(f"Kafka consumer başlatılırken hata oluştu: {e}")

    def start_kafka_consumer(self):
        from .KafkaConsumer import start_consumer
        """Kafka consumer başlatılır."""
        try:
            start_consumer()
            logging.info("Kafka Consumer başarıyla başlatıldı.")
        except Exception as e:
            logging.error(f"Kafka consumer başlatma hatası: {e}")
