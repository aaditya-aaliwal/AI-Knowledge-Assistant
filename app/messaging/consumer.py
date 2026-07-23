import json

from app.config import settings
from app.logger import logger
from app.messaging.rabbitmq_client import get_rabbitmq_channel
from pathlib import Path

from app.services.document_ingestion_service import DocumentIngestionService

from app.services.pdf_service import PDFService
from app.services.chunking_service import ChunkingService
from app.services.embedding_service import EmbeddingService
from app.vectorstore.vector_store import VectorStore

class RabbitMQConsumer:

    def start(self) -> None:

        connection = None
        
        try:
            connection, channel = get_rabbitmq_channel()
            pdf_service = PDFService()
            
            chunking_service = ChunkingService()
            
            embedding_service = EmbeddingService()
            
            vector_store = VectorStore()


            document_ingestion_service = DocumentIngestionService(
                pdf_service=pdf_service,
                chunking_service=chunking_service,
                embedding_service=embedding_service,
                vector_store=vector_store,
            )
         

            channel.basic_qos(
                prefetch_count=1
            )

            def callback(ch, method, properties, body):

                try:
                    message = json.loads(body)

                    logger.info(
                        f"Received message: {message}"
                    )

                    file_path = Path(message["file_path"])

                    document_ingestion_service.ingest_document(
                        file_path=file_path
                    )

                    ch.basic_ack(
                        delivery_tag=method.delivery_tag
                    )

                    logger.info(
                        "Message processed successfully."
                    )

                except Exception:
                    logger.exception(
                        "Failed to process RabbitMQ message."
                    )

                    ch.basic_nack(
                        delivery_tag=method.delivery_tag,
                        requeue=True
                    )

            channel.basic_consume(
                queue=settings.RABBITMQ_QUEUE,
                on_message_callback=callback,
                auto_ack=False
            )

            logger.info(
                "RabbitMQ Consumer started. Waiting for messages..."
            )

            channel.start_consuming()

        except KeyboardInterrupt:
            logger.info(
                "RabbitMQ Consumer stopped."
            )

        except Exception:
            logger.exception(
                "RabbitMQ Consumer failed."
            )
            raise

        finally:
            if connection and connection.is_open:
                connection.close()

                logger.info(
                    "RabbitMQ connection closed."
                )


consumer = RabbitMQConsumer()