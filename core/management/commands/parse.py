from django.core.management.base import BaseCommand
from core.parser import XMLParser
import requests
from core.tasks import update_podcast, update_all_podcasts


class Command(BaseCommand):
    help = "Parse and update podcast data"

    def handle(self, *args, **options):
        
        xml_parser = XMLParser('https://rss.art19.com/apology-line')

        # channel_data = xml_parser.seve_channel_in_database()
        
        # xml_parser.item_parser(channel_data)
        
        # xml_parser.save_items_in_database()
        

        # xml_parser.xml_link_parse()
        
        update_podcast.delay('https://rss.art19.com/apology-line')
        update_all_podcasts.delay() 
                
            
        # except Exception as e:
        #     self.stdout.write(
        #         self.style.ERROR(
        #             f"Error while parsing and updating podcast rss data models \n {e})"
        #         )
        #     )