from django.core.management.base import BaseCommand
from core.parser import XMLParser
import requests
from core.tasks import update_podcast, update_all_podcasts
from accounts.publisher import Publish
from accounts.consumer import login_consume, register_consume, update_podcast_consume
import threading


class Command(BaseCommand):
    help = "Parse and update podcast data"

    def handle(self, *args, **options):
        
        login_thread = threading.Thread(target=login_consume)
        register_thread = threading.Thread(target=register_consume)
        update_podcast_thread = threading.Thread(target=update_podcast_consume)
        
        login_thread.start()
        register_thread.start()
        update_podcast_thread.start()
        
        # xml_parser = XMLParser('https://rss.art19.com/apology-line')
        
        # xml_link = xml_parser.xml_link_parse()
        # # # print(xml_link)

        # channel_data = xml_parser.seve_channel_in_database(xml_link)
        # # # print(channel_data)
        
        # xml_parser.item_parser(channel_data, xml_link)
        
        # xml_parser.save_items_in_database()
        
        # xml_parser.update_episodes()
        

        # xml_parser.xml_link_parse()
        
        # The two below links is for celery:
        # update_podcast.delay('https://rss.art19.com/apology-line')
        # update_all_podcasts.delay() 
        # update_all_podcasts.delay()
            
        # except Exception as e:
        #     self.stdout.write(
        #         self.style.ERROR(
        #             f"Error while parsing and updating podcast rss data models \n {e})"
        #         )
        #     )