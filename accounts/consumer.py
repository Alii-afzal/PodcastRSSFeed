import pika
import json
import time
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User, NotificationInfo, Notification
from interactions.models import BookMark, Subscribe
from config import settings

from core.models import Channel

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
    
def register_callback(channel, method, properties, body):
    data = json.loads(body)
    user = User.objects.get(email=data['email'])
    notification_info = NotificationInfo.objects.create(message=data['message'])
    Notification.objects.create(user = user, message = notification_info)

def register_consume():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST))
    channel = connection.channel()

    channel.queue_declare(queue='register')
    channel.basic_consume(queue='register', on_message_callback=login_callback)

    channel.start_consuming()


# def update_podcast_callback(channel, method, properties, body):
#     data = json.loads(body)
    
#     channel_id = data['podcast']
    
#     subscribers = Subscribe.objects.filter(channel=Channel.objects.get(id=channel_id))
#     if subscribers.exists():
#         for subscriber in subscribers:
#             notification = NotificationInfo.objects.create(message = data['message'])
#             user = User.objects.get(id=subscriber.user.id)
#             Notification.objects.create(user = user, message = notification)


def update_podcast_callback(channel, method, properties, body):
    try:
        data = json.loads(body)
        channel_id = data['podcast']
        # user = User.objects.get(email=data['email'])
        subscribers = Subscribe.objects.filter(channel=Channel.objects.get(id=channel_id))
        if subscribers.exists():
            for subscriber in subscribers:
                notification = NotificationInfo.objects.create(message=data['message'])
                user = User.objects.get(id=subscriber.user.id)
                print(user)
                Notification.objects.create(user=user, message=notification)
    except Exception as e:
        print(e)
    finally:
        channel.basic_ack(delivery_tag=method.delivery_tag)

def update_podcast_consume():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST))
    channel = connection.channel()

    channel.queue_declare(queue='update_podcast')
    channel.basic_consume(queue='update_podcast', on_message_callback=update_podcast_callback)

    channel.start_consuming()
    
