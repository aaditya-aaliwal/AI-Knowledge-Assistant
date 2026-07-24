import pika
from pika.adapters.blocking_connection import BlockingChannel

from app.config import settings
from app.logger import logger


def get_rabbitmq_channel() -> tuple[pika.BlockingConnection, BlockingChannel]:
    """
    Create a RabbitMQ connection and return
    both the connection and channel.
    """

    try:
        credentials = pika.PlainCredentials(
            username=settings.RABBITMQ_USERNAME,
            password=settings.RABBITMQ_PASSWORD
        )

        connection_parameters = pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            credentials=credentials
        )

        connection = pika.BlockingConnection(connection_parameters)

        channel = connection.channel()

        channel.queue_declare(
            queue=settings.RABBITMQ_QUEUE,
            durable=True
        )

        logger.info(
            "RabbitMQ connection established successfully."
        )

        return connection, channel

    except Exception as exception:
        logger.exception(
            "Failed to connect to RabbitMQ."
        )
        raise exception