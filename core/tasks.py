import requests
from celery import shared_task, Task
from .parser import XMLParser
from .models import Channel, Episode, XmlLink
import logging


logger = logging.getLogger(__name__)

class RetryTask(Task):
    autoretry_for = (Exception,)
    retry_kwargs = {'max_retries': 5}
    retry_backoff = 2
    retry_jitter = False
    task_acks_late = True
    worker_concurrency = 4
    prefetch_multiplier = 1


@shared_task(bind=True, base=RetryTask)
def update_all_podcasts(self):
    xml_links = XmlLink.objects.all()

    for xml_link in xml_links:
        print(xml_link)
        url = xml_link.xml_link
        update_podcast.delay(url)

    return "URLs sent to parsing!"

@shared_task(bind=True, base=RetryTask)
def update_podcast(self, url):
    data = requests.get(url).text
    parser = XMLParser(xml_link=data)
    parser.update_episodes()

    return 'Update podcast task is complete'
