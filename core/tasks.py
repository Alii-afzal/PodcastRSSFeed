# from celery import shared_task
# from .parser import XMLParser
# from .models import Channel, Episode, XmlLink

# # from celery.utils.log import get_task_logger


# class RetryTask(Task):
#     autoretry_for = (Exception,)
#     retry_kwargs = {'max_retries': 5}
#     retry_backoff = 2


# @shared_task
# def update_all_podcast():
#     url_list = Channel.objects.all().values_list('xml_link')
#     for url in url_list:
#         update_podcast.delay(url)
#     return "URL sent for parse data in it."

# @shared_task(bind=True, base=RetryTask)
# def update_podcast(self, url):
#     data = request.get(url).text
#     parser = XMLParser()