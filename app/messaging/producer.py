import json

from app.config import settings
from app.logger import logger
from app.messaging.rabbitmq_client import get_rabbitmq_channel
import pika



class RabbitMQProducer:

    def publish(
        self,
        message: dict
    ) -> None:

        connection = None

        try:
            connection, channel = get_rabbitmq_channel()

            channel.basic_publish(
                exchange="",
                routing_key=settings.RABBITMQ_QUEUE,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=pika.DeliveryMode.Persistent
                )
            )

            logger.info(
                "Message published to RabbitMQ."
            )

        except Exception:
            logger.exception(
                "Failed to publish RabbitMQ message."
            )
            raise

        finally:
            if connection and connection.is_open:
                connection.close()


producer = RabbitMQProducer()