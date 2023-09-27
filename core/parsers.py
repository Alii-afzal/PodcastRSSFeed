from abc import ABC, abstractmethod
from datetime import datetime
import requests
import xml.etree.ElementTree as ET

class Parser(ABC):
    def __init__(self, xml_data):
        self.itunes_namespace = {'itunes':'http://www.itunes.com/dtds/podcast-1.0.dtd'}
        self.root = ET.fromstring(xml_data)
        self.channel_data= self.root.find('channel')

    def get_element_text(self, element, tag):
        sub_element = element.find(tag, namespaces=self.itunes_namespace)    
        return sub_element.text if sub_element is not None else ''
    
    @staticmethod
    def get_element_attr(element, tag, attr):
        sub_element = element.find(tag)    
        return sub_element.get(attr) if sub_element is not None else ''
    
    def parse_date(self, date_str):
        if date_str:
            return datetime.strptime(date_str)
        return None
    
    def parse_channel(self):
        title = self.get_element_text(self.channel_data, 'title')
        subtitle = self.get_element_text(self.channel_data, 'itunes:subtitle')
        description = self.get_element_text(self.channel_data, 'description')
        pub_date_str = self.get_element_text(self.channel_data, 'pubDate')
        pub_date = self.parse_date(pub_date_str)
        image = self.get_element_attr(self.channel_data, 'itunes:image', 'href')
        author = self.get_element_text(self.channel_data, 'itunes:author')
        source = self.get_element_text(self.channel_data, 'link')
        language = self.get_element_text(self.channel_data, 'language')
        owner = self.get_element_text(self.channel_data, 'itunes:owner/itunes:name')
        
        return {
            'title': title,
            'subtitle': subtitle,
            'description' : description,
            'pub_date' : pub_date,
            'image' : image,
            'language' : language,
            'author' : author,
            'source' : source,
            'owner' : owner,
        }

class PodcastParser(Parser): 
    def item_parser(self, item):
        title = self.get_element_text(item, 'title')
        subtitle = self.get_element_text(item, 'itunes:subtitle')
        description = self.get_element_text(item, 'description')
        guid = self.get_element_text(item, 'guid')
        pub_date_str = self.get_element_text(self.channel_data, 'pubDate')
        pub_date = self.parse_date(pub_date_str)
        duration = self.get_element_text(item, 'itunes:duration')
        audio_file = self.get_element_attr(item, 'enclosure', 'url')
        image = self.get_element_attr(item, 'itunes:image', 'href')
        explicit = True if (self.get_element_text(item, 'itunes:explicit')).lower() in ('yes' or 'true') else False
        
        return {
            'title': title,
            'subtitle': subtitle,
            'description' : description,
            'guid' : guid,
            'pub_date' : pub_date,
            'duration' : duration,
            'audio_file' : audio_file,
            'image' : image,
            'explicit' : explicit,
        }
         
    def parse_xmls(self):
        channel_data = self.parse_channel()
        items = list()
        for item in self.channel_data.findall('item'):
            item_data = self.item_parser(item)
            items.append(item_data)
        return {'channel_data':channel_data, 'podcast_data':items}        


response = requests.get('https://rss.art19.com/apology-line')
xml_data = response.text
parsed_data = PodcastParser(xml_data).parse_xmls()
print(parsed_data)