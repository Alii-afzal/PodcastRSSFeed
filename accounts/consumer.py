import pika
import json
import time
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User, NotificationInfo, Notification
from interactions.models import BookMark
from config import settings

def login_callback(ch, method, properties, body):
    data = json.loads(body)
    user = User.objects.get(email=data['email'])
    notification_info = NotificationInfo.objects.create(message=data['message'])
    Notification.objects.create(user=user, message=notification_info)
    
def login_consume():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST))
    channel = connection.channel()
    
    channel.queue_declare(queue='login')
    channel.basic_consume(queue='login', on_message_callback=login_callback)
    
    channel.start_consuming()

def register_consume():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST))
    chanel = connection.channel()

    chanel.queue_declare(queue='register')
    chanel.basic_consume(queue='register', on_message_callback=login_callback)

    chanel.start_consuming()