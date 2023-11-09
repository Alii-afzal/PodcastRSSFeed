from datetime import datetime
import requests
import xml.etree.ElementTree as ET
from .models import Channel, Episode, Category, XmlLink
from accounts.publisher import Publish


class XMLParser():
    def __init__(self, xml_link):
        self.xml_link = xml_link
        self.response = requests.get(self.xml_link)
        self.xml_data = self.response.text
        self.root = ET.fromstring(self.xml_data)
        self.itunes_namespace = {'itunes':'http://www.itunes.com/dtds/podcast-1.0.dtd'}
        self.all_episodes = []
        self.channel_data = []
    
    def xml_link_parse(self):
        xml_link = self.xml_link
        xml_link_data,_ = XmlLink.objects.get_or_create(xml_link=xml_link)
        return xml_link_data
         
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

    def channel_parser(self, xml_link_obj):
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

        category,_ = Category.objects.get_or_create(title=category)
        
    
        channel,_ = Channel.objects.get_or_create(
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
                xml_link=xml_link_obj   
        ) 
        
        return channel
     
    def seve_channel_in_database(self, xml_link):
        channel_data = self.channel_parser(xml_link)
        return channel_data
        
    def item_parser(self, channel_obj, xml_link_obj):
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
                'channel': channel_obj,
                'subtitle': subtitle,
                'description': description,
                'pubDate': pubDate,
                'image': image,
                'duration': duration,
                'audio_file': audio_file,
                'guid': guid,
                'explicit': explicit,
                'xml_link': xml_link_obj
            }

            self.all_episodes.append(episode_data)  
        return self.all_episodes

       
    def save_items_in_database(self):
        for episode_data in self.all_episodes:
            Episode.objects.get_or_create(**episode_data)
        
    def update_episodes(self):
        xml_link_data = self.xml_link_parse()
        channel_data = self.seve_channel_in_database(xml_link=xml_link_data)
        new_episodes = self.item_parser(channel_obj=channel_data,xml_link_obj=xml_link_data)

        existing_episodes = Episode.objects.filter(xml_link=xml_link_data)
        existing_guids = set(existing.guid for existing in existing_episodes)

        
        for episode in new_episodes:
            if episode['guid'] not in existing_guids:
                Episode.objects.create(**episode)   
                existing_guids.add(episode['guid'])
                Publish().update_podcast(channel_data)