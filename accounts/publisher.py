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
        
    def login(self, email, request_META):
        notif = {
            'email' : email,
            'message' : f"{email} is login; {request_META}",
            # 'user_agent': request_META,
            'routing_key': 'login'
        }
        
        self.response = None
        self.channel.basic_publish(exchange='', routing_key = 'login',
                                   properties = pika.BasicProperties(delivery_mode=2), body = json.dumps(notif))
        
        
    def register(self, email, request_META):
        notification={
            'email' : email,
            'message' : f"{email} is register; {request_META}",
            'routing_key': 'register'
        }
        self.response = None
        self.channel.basic_publish(exchange = '', routing_key = 'register',
                                   properties = pika.BasicProperties(delivery_mode=2), body = json.dumps(notification))
        
        
    def update_podcast(self, podcast):
        notification={
            'podcast' : podcast.id,
            'message' : f"{podcast.title} has new episodes",
            # 'email' : email,
            'routing_key': 'update_podcast'
        }
        self.response = None
        self.channel.basic_publish(exchange = '', routing_key = 'update_podcast',
                                    properties = pika.BasicProperties(delivery_mode=2), body = json.dumps(notification))