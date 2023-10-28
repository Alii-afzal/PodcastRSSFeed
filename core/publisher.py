import pika
import uuid
import json

class Publish:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = connection.channel()
        result = self.channel.queue_declare(queue = '', exclusive = True)
        self.qname = result.method.queue
        
    def login(self, email, request_META):
        notif = {
            'email' : email,
            'message' : f"{email} is login; {request_META}"
        }
        
        self.response = None
        self.channel.basic_publish(exchange='', routing_key = 'login', properties = pika.BasicProperties(delivery_mode=2), body = json.dumps(notif))
        
    def register(self, email, request_META):
        notification={
            'email' : email,
            'message' : f"{email} is register; {request_META}"
        }
        self.response = None
        self.chanel.basic_publish(exchange = '', routing_key = 'register',properties = pika.BasicProperties(delivery_mode=2), body = json.dumps(notification))
        
    def update_podcast(self, podcast):
        notification={
            'podcast' : podcast,
            'message' : f"{podcast} has new episodes"
        }
        self.response = None
        self.chanel.basic_publish(exchange = '', routing_key = 'update_podcast', properties = pika.BasicProperties(delivery_mode=2), body =notification)