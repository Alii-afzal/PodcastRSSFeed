import requests
from celery import shared_task, Task
from .parser import XMLParser
from .models import Channel, Episode, XmlLink
import logging
from .task_logs import log_task_info



class RetryTask(Task):
    autoretry_for = (Exception,)
    retry_kwargs = {'max_retries': 5}
    retry_backoff = 2
    # retry_jitter = False
    task_acks_late = True
    worker_concurrency = 4
    # prefetch_multiplier = 1
    
    def retry(self, args=None, kwargs=None, exc=None, throw=True,
              eta=None, countdown=None, max_retries=None, **options):
        retry_count = self.request.retries
        retry_eta = eta or (countdown and f'countdown={countdown}') or 'default'
        log_task_info(self.name, 'warning', f'Retrying task {self.name} (retry {retry_count}) in {retry_eta} seconds',self.request.id, args, kwargs, exception=exc, retry_count=retry_count, max_retries=max_retries, retry_eta=retry_eta)

        super().retry(args, kwargs, exc, throw, eta, countdown, max_retries, **options)



@shared_task(bind=True, base=RetryTask)
def update_all_podcasts(self):
    xml_links = XmlLink.objects.all()

    for xml_link in xml_links:
        url = xml_link.xml_link
        update_podcast.delay(url)

    # logger.error('Update aoo podcasts done successfully')
    return "All episodes updated successfully."

@shared_task(bind=True, base=RetryTask)
def update_podcast(self, url):
    parser = XMLParser(xml_link=url)
    parser.update_episodes()

    return 'Update podcast task is complete'
