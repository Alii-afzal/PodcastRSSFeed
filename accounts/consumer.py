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


def login_consume():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST))
    channel = connection.channel()
    
    channel.queue_declare(queue='login')
    channel.basic_consume(queue='login', on_message_callback=login_callback)
    
    channel.start_consuming()