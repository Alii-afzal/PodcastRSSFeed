import pika
import uuid
import json

class Publish:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = connection.channel()
        result = self.channel.queue_declare(queue = '', exclusive = True)
        self.qname = result.method.queue
        
 