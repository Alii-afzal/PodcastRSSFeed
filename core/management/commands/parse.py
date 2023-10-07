from django.core.management.base import BaseCommand
from core.parser import channel_parser, item_parser
from core.parsers import Parser, PodcastParser
import requests

class Command(BaseCommand):
    help = "Parse and update podcast data"

    def handle(self, *args, **options):
        try:
            # podcast_parse_task.delay()
            
            # channel_parser()
            item_parser()
            # response = requests.get('https://rss.art19.com/apology-line')
            # xml_data = response.text 
            # parser = Parser(xml_data)
            # parser.parse_channel()
            # podcastparser = PodcastParser(xml_data)
            # podcastparser.parse_xmls()
            
                
            self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully parsed and updated podcast data for all models)"
                    )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f"Error while parsing and updating podcast rss data models \n {e})"
                )
            )