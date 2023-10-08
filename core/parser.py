from datetime import datetime
import requests
import xml.etree.ElementTree as ET
from .models import Channel, Episode, Category

class XMLParser():
    response = requests.get('https://rss.art19.com/apology-line')
    xml_data = response.text
    root = ET.fromstring(xml_data)
    itunes_namespace = {'itunes':'http://www.itunes.com/dtds/podcast-1.0.dtd'}
        
    def convert_text_to_datefield(date_str):
        custom_format='%a, %d %b %Y %H:%M:%S %z'
        if date_str:
            return datetime.strptime(date_str, custom_format)
        else:
            return None

    def convert_text_to_boolianfield(explicit_str):
        if explicit_str == 'yes':
            return True
        elif explicit_str == 'no':
            return False
        else:
            return None

    def XML_link_parser():
        pass

    def channel_parser():
        
        for elm in root.findall(".//channel", itunes_namespace):
            title = elm.find('.//title').text if elm.find('.//title') is not None else None
            subtitle = elm.find('.//subtitle').text if elm.find('.//subtitle') is not None else None
            description = elm.find('.//description').text if elm.find('.//description') is not None else None
            pubDate = convert_text_to_datefield(elm.find('.//pubDate').text) if elm.find('.//pubDate') is not None else None
            image = elm.find('.//itunes:image', itunes_namespace).attrib.get('href') if elm.find('.//itunes:image', itunes_namespace) is not None else None
            language = elm.find('.//language').text if elm.find('.//language') is not None else None
            author = elm.find('.//itunes:author', itunes_namespace).text if elm.find('.//itunes:author', itunes_namespace) is not None else None
            category = elm.find('.//itunes:category', itunes_namespace).get('text') if elm.find('.//itunes:category', itunes_namespace) is not None else None
            source =elm.find('.//link').text if elm.find('.//link') is not None else None
            owner = convert_text_to_boolianfield(elm.find('.//itunes:owner/itunes:name', itunes_namespace)) if elm.find('.//itunes:owner/itunes:name', itunes_namespace) is not None else None

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
        
    def item_parser():
        all_episodes = []  # Create a list to store all Episode dictionaries
        for elm in root.findall(".//item", itunes_namespace):
            title = elm.find('.//title').text if elm.find('.//title') is not None else None
            subtitle = elm.find('.//subtitle').text if elm.find('.//subtitle') is not None else None
            description = elm.find('.//description').text if elm.find('.//description') is not None else None
            pubDate = convert_text_to_datefield(elm.find('.//pubDate').text) if elm.find('.//pubDate') is not None else None
            image = elm.find('.//itunes:image', itunes_namespace).attrib.get('href') if elm.find('.//itunes:image', itunes_namespace) is not None else None
            duration = elm.find('.//itunes:duration', itunes_namespace).text if elm.find('.//itunes:duration', itunes_namespace) is not None else None
            audio_file = elm.find('.//enclosure').attrib.get('url') if elm.find('.//enclosure') is not None else None
            guid = elm.find('.//guid').text if elm.find('.//guid') is not None else None
            explicit = convert_text_to_boolianfield(elm.find('.//itunes:explicit', itunes_namespace).text) if elm.find('.//itunes:explicit', itunes_namespace) is not None else None

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