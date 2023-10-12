from celery import shared_task
from .parser import XMLParser
from .models import Channel, Episode, XmlLink
# from celery.utils.log import get_task_logger



@shared_task
def update_all_podcast():
    url_list = Podcast.objects.all().values_list('podcast_url')
    for url in url_list:
        update_podcast.delay(url)