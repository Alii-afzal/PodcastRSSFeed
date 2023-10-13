from django.core.management.base import BaseCommand
from core.parser import XMLParser
import requests

class Command(BaseCommand):
    help = "Parse and update podcast data"

    def handle(self, *args, **options):
        try:
            xml_parser = XMLParser()

            xml_parser.item_parser()
            xml_parser.save_items_in_database()
            
            xml_parser.channel_parser()
            xml_parser.seve_channel_in_database()

                
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