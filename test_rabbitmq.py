from app.messaging.producer import producer

producer.publish(
    {
        "file_path": "uploads/python.pdf",
        "filename": "python.pdf"
    }
)

print("Message Sent Successfully")