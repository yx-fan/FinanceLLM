from datetime import datetime
from mongoengine import Document, StringField, DateTimeField

class DataIngestionLog(Document):
    source = StringField(required=True)  # Source of the data (e.g., Yahoo Finance, Wikipedia)
    status = StringField(choices=["SUCCESS", "FAILED"])  # Status of the ingestion
    message = StringField()  # Any message related to the ingestion
    timestamp = DateTimeField(default=datetime.now)  # Timestamp of the log entry