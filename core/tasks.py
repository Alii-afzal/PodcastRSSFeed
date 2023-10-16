import requests
from celery import shared_task, Task
from .parser import XMLParser
from .models import Channel, Episode, XmlLink


class RetryTask(Task):
    autoretry_for = (Exception,)
    retry_kwargs = {'max_retries': 5}
    retry_backoff = 2
    retry_jitter = False
    task_acks_late = True
    worker_concurrency = 4
    prefetch_multiplier = 1

@shared_task(bind=True, base=RetryTask)
def update_podcast(self, url):
    data = requests.get(url).text
    parser = XMLParser(xml_link=data)
    parser.update_episodes()

    return 'Update podcast task is complete'
