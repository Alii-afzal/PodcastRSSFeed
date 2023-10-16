from datetime import datetime
import requests
import xml.etree.ElementTree as ET
from .models import Channel, Episode, Category, XmlLink

class XMLParser():
    def __init__(self, xml_link=None):
        self.xml_link ='https://rss.art19.com/apology-line'
        self.response = requests.get(self.xml_link)
        self.xml_data = self.response.text
        self.root = ET.fromstring(self.xml_data)
        self.itunes_namespace = {'itunes':'http://www.itunes.com/dtds/podcast-1.0.dtd'}
        self.all_episodes = []
        self.channel_data = []
        self.category_data = []
    
    def xml_link_parse(self):
        xml_link = self.xml_link
        XmlLink.objects.create(xml_link=xml_link)
         
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

    def xml_link_parse(self):
        xml_link = self.xml_link
        XmlLink.objects.create(xml_link=xml_link)
    
    # def get_element_from_channel(self, tag):
    #     for elm in self.root.findall(".//channel", self.itunes_namespace):
    #         element = elm.find(tag).text if elm.find(tag) is not None else None
    #     return element

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
            xml_link = self.xml_link
    
    
        category = Category.objects.create(title=category)
        
        channel = {
                'title' : title,
                'subtitle' :subtitle,
                'description' :description,
                'pubDate' : pubDate,
                'image' : image,
                'language' : language,
                'author' : author,
                'category' : category,
                'source' : source,
                'owner' : owner,
                'xml_link' : xml_link,   
        }
        self.channel_data.append(channel)
        return self.channel_data, self.category_data
        return channel
    
    def seve_channel_in_database(self):
        for ch in self.channel_data:
            Channel.objects.get_or_create(**ch)
        # channel_instance = Channel()
        # channel_instance.objects.get_or_create()

    
    # def save_category_in_database(self):
    #     for category in self.category_data:
    #         Category.objects.create(**category)
        
    def item_parser(self):
        # channel_parser = self.channel_parser()
        # channel = Channel.objects.get(source=self.channel_data['source'])
        
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
                # 'channel': channel,
                'subtitle': subtitle,
                'description': description,
                'pubDate': pubDate,
                'image': image,
                'duration': duration,
                'audio_file': audio_file,
                'guid': guid,
                'explicit': explicit,
            }

            self.all_episodes.append(episode_data)  
        return self.all_episodes

       
    def save_items_in_database(self):
        for episode_data in self.all_episodes:
            Episode.objects.get_or_create(**episode_data)
        
    def update_episodes(self):
        new_episodes = self.item_parser()

        existing_episodes = Episode.objects.filter()
        existing_guids = set(existing.guid for existing in existing_episodes)

        for episode in new_episodes:
            if episode['guid'] not in existing_guids:
                print(episode['guid'])
                Episode.objects.create(**episode)   
                existing_guids.add(episode['guid'])
 
# xml_parser = XMLParser() 