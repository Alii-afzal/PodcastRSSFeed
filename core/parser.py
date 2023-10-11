from datetime import datetime
import requests
import xml.etree.ElementTree as ET
from .models import Channel, Episode, Category

class XMLParser():
    def __init__(self):
        self.response = requests.get('https://rss.art19.com/apology-line')
        self.xml_data = self.response.text
        self.root = ET.fromstring(self.xml_data)
        self.itunes_namespace = {'itunes':'http://www.itunes.com/dtds/podcast-1.0.dtd'}
            
    def convert_text_to_datefield(self, date_str):
        custom_format='%a, %d %b %Y %H:%M:%S %z'
        if date_str:
            return datetime.strptime(date_str, custom_format)
        else:
            return None

    def convert_text_to_boolianfield(self, explicit_str):
        if explicit_str == 'yes':
            return True
        elif explicit_str == 'no':
            return False
        else:
            return None

    # def XML_link_parser():
    #     pass

    def channel_parser(self):
        for elm in self.root.findall(".//channel", self.itunes_namespace):
            title = elm.find('.//title').text if elm.find('.//title') is not None else None
            subtitle = elm.find('.//subtitle').text if elm.find('.//subtitle') is not None else None
            description = elm.find('.//description').text if elm.find('.//description') is not None else None
            pubDate = self.convert_text_to_datefield(elm.find('.//pubDate').text) if elm.find('.//pubDate') is not None else None
            image = elm.find('.//itunes:image', self.itunes_namespace).attrib.get('href') if elm.find('.//itunes:image', self.itunes_namespace) is not None else None
            language = elm.find('.//language').text if elm.find('.//language') is not None else None
            author = elm.find('.//itunes:author', self.itunes_namespace).text if elm.find('.//itunes:author', self.itunes_namespace) is not None else None
            category = elm.find('.//itunes:category', self.itunes_namespace).get('text') if elm.find('.//itunes:category', self.itunes_namespace) is not None else None
            source =elm.find('.//link').text if elm.find('.//link') is not None else None
            owner = self.convert_text_to_boolianfield(elm.find('.//itunes:owner/itunes:name', self.itunes_namespace)) if elm.find('.//itunes:owner/itunes:name', self.itunes_namespace) is not None else None

        category = Category(
            title=category
        )
        category.save()
        
        channel = Channel(
                title = title,
                subtitle = subtitle,
                description = description,
                pubDate = pubDate,
                image = image,
                language = language,
                author = author,
                category=category,
                source = source,
                owner = owner,   
        ) 

        channel.save()
        
    def item_parser(self):
        all_episodes = []
        for elm in self.root.findall(".//item", self.itunes_namespace):
            title = elm.find('.//title').text if elm.find('.//title') is not None else None
            subtitle = elm.find('.//subtitle').text if elm.find('.//subtitle') is not None else None
            description = elm.find('.//description').text if elm.find('.//description') is not None else None
            pubDate = self.convert_text_to_datefield(elm.find('.//pubDate').text) if elm.find('.//pubDate') is not None else None
            image = elm.find('.//itunes:image', self.itunes_namespace).attrib.get('href') if elm.find('.//itunes:image', self.itunes_namespace) is not None else None
            duration = elm.find('.//itunes:duration', self.itunes_namespace).text if elm.find('.//itunes:duration', self.itunes_namespace) is not None else None
            audio_file = elm.find('.//enclosure').attrib.get('url') if elm.find('.//enclosure') is not None else None
            guid = elm.find('.//guid').text if elm.find('.//guid') is not None else None
            explicit = self.convert_text_to_boolianfield(elm.find('.//itunes:explicit', self.itunes_namespace).text) if elm.find('.//itunes:explicit', self.itunes_namespace) is not None else None

            episode_data = {
                'title': title,
                'subtitle': subtitle,
                'description': description,
                'pubDate': pubDate,
                'image': image,
                'duration': duration,
                'audio_file': audio_file,
                'guid': guid,
                'explicit': explicit,
            }

            all_episodes.append(episode_data)  # Append the episode data to the list

        # Create Episode objects using the data collected in the loop
        for episode_data in all_episodes:
            Episode.objects.create(**episode_data)
            
    # def update_episode(self):
    #     new_items=[]
    #     self.item_parser()
    #     for item in self.all_episodes:
    #         if not Episode.objects.filter(guid=item['guid']).exists():
    #             new_items.append(item)
    #     # for 
    