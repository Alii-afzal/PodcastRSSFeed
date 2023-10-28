import pika
import uuid
import json

from config import settings

class Publish:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST, port=settings.RABBITMQ_PORT))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue = '', exclusive = True)
        self.qname = result.method.queue