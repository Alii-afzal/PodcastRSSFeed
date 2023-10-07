# from celery import shared_task
# from .parser import XMLParser
# from .models import Channel, Episode, XmlLink
# from celery.utils.log import get_task_logger

# logger= get_task_logger(__name__)

# @shared_task(bind=True)
# def update_podcast(self):
#     xml_urls=XmlLink.objects.all()
#     try:
#         for xml_url in xml_urls:
#             pass
        
#     except:
#         logger.info()
#         self.retry()