from datetime import datetime
import requests
import xml.etree.ElementTree as ET
from .models import Channel, Episode, Category

def convert_text_to_datefield(date_str):
    custom_format='%a, %d %b %Y %H:%M:%S %z'
    if date_str:
        return datetime.strptime(date_str, custom_format).strftime(custom_format)
    else:
        return None

def convert_text_to_boolianfield(explicit_str):
    if explicit_str == 'yes':
        return True
    elif explicit_str == 'no':
        return False
    else:
        return None
        

def channel_parser():
    response = requests.get('https://rss.art19.com/apology-line')
    xml_data = response.text
    root = ET.fromstring(xml_data)
    itunes_namespace = {'itunes':'http://www.itunes.com/dtds/podcast-1.0.dtd'}
    
    title = [elm.text for elm in root.findall(".//channel/title", itunes_namespace)],
    # print(title)
    
    
    
    for elm in root.findall(".//channel", itunes_namespace):
        if elm.findall('.//title'):
            title = elm.find('.//title').text
        else:
            title = None
        # print(title)
        if elm.findall('.//subtitle'):
            subtitle = elm.find('.//subtitle').text
        else:
            subtitle = None
        # print(subtitle)
        if elm.findall('.//description'):
            description = elm.find('.//description').text
        else:
            description = None
        # print(description)
        if elm.findall('.//pubDate'):
            pubDate = convert_text_to_datefield(elm.find('.//pubDate').text)
        else:
            pubDate = None
        print(pubDate)
        if elm.findall('.//itunes:image', itunes_namespace):
            image = elm.find('.//itunes:image', itunes_namespace).attrib
        else:
            image = None
        # print(image)
        if elm.findall('.//itunes:author', itunes_namespace):
            author = elm.find('.//itunes:author', itunes_namespace).text
        else:
            author = None
        # print(author)
        if elm.findall('.//itunes:category', itunes_namespace):
            category = elm.find('.//itunes:category', itunes_namespace).get('text')
        else:
            category = None
        # print(category)
        if elm.findall('.//link'):
            source = elm.find('.//link').text
        else:
            source = None
        # print(source)
        if elm.findall('.//language'):
            language = elm.find('.//language').text
        else: 
            language = None
        # print(language)
        if elm.findall('.//itunes:owner/itunes:name', itunes_namespace):
            owner = elm.find('.//itunes:owner/itunes:name', itunes_namespace).text
        else:
            owner = None
        # print(convert_text_to_boolianfield(owner))
        # print(owner)
    
    category = Category(
        title=category
    )
    category.save()
    
    channel = Channel(
            title = title,
            subtitle = subtitle,
            description = description,
            pubDate = convert_text_to_datefield(pubDate),
            image = image,
            language = language,
            author = author,
            category=category,
            source = source,
            owner = owner,   
    ) 

    channel.save()
    
    # channel = Channel(
    #     title = [elm.text for elm in root.findall(".//channel/title", itunes_namespace)],
    #     # print(title),
    #     subtitle = [elm.text for elm in root.findall(".//channel/subtitle", itunes_namespace)],
    #     # print(subtitle)
    #     description = [elm.text for elm in root.findall(".//channel/description", itunes_namespace)],
    #     # print(description)
    #     pubDate = [elm.text for elm in root.findall(".//channel/pubDate", itunes_namespace)],
    #     # print(pubDate)
    #     image = [elm.attrib for elm in root.findall(".//channel/itunes:image", itunes_namespace)],
    #     # print(image)
    #     author = [elm.text for elm in root.findall(".//channel/itunes:author", itunes_namespace)],
    #     # print(author)
    #     source = [elm.text for elm in root.findall(".//channel/link", itunes_namespace)],
    #     # print(source)
    #     language = [elm.text for elm in root.findall(".//channel/language", itunes_namespace)],
    #     # print(language)
    #     owner = [elm.text for elm in root.findall(".//channel/itunes:owner/itunes:name", itunes_namespace)],
    # # print(owner)
    # )
    # channel.save()
    # return {
    #         'title': title,
    #         'subtitle': subtitle,
    #         'description' : description,
    #         'puDate' : pubDate,
    #         'image' : image,
    #         'language' : language,
    #         'author' : author,
    #         'source' : source,
    #         'owner' : owner,
    #     }
    
    


def item_parser():
    response = requests.get('https://rss.art19.com/apology-line')
    xml_data = response.text
    root = ET.fromstring(xml_data)
    itunes_namespace = {'itunes':'http://www.itunes.com/dtds/podcast-1.0.dtd'}
    
    title = [elm.text for elm in root.findall(".//item/title", itunes_namespace)],
    # print(title)
    
    for elm in root.findall(".//item", itunes_namespace):
        if elm.findall('.//title'):
            title = elm.find('.//title').text
        else:
            title = None
        # print(title)
        if elm.findall('.//subtitle'):
            subtitle = elm.findall('.//subtitle').text
        else:
            subtitle = None
        # print(subtitle)
        if elm.findall('.//description'):
            description = elm.find('.//description').text
        else:
            description = None
        # print(description)
        if elm.findall('.//pubDate'):
            pubDate = convert_text_to_datefield(elm.find('.//pubDate').text)
        else:
            pubDate = None
        # print(pubDate)
        if elm.findall('.//itunes:image', itunes_namespace):
            image = elm.find('.//itunes:image', itunes_namespace).attrib.get('href')
        else:
            image = None
        # print(image)
        if elm.findall('.//itunes:duration', itunes_namespace):
            duration = elm.find('.//itunes:duration', itunes_namespace).text
        else:
            duration = None
        # print(duration)
        if elm.findall('.//enclosure'):
            audio_file = elm.find('.//enclosure').attrib.get('url')
        else:
            audio_file = None
        # print(audio_file)
        if elm.findall('.//guid'):
            guid = elm.find('.//guid').text
        else:
            guid = None 
        # print(guid)
        if elm.findall('.//itunes:explicit', itunes_namespace):
            explicit = convert_text_to_boolianfield(elm.find('.//itunes:explicit', itunes_namespace).text)
        else:
            explicit = None
        # print(explicit)
        
    item = Episode.objects.create(
        **{
            'title': title,
            'subtitle': subtitle,
            'description' : description,
            'guid' : guid,
            'pubDate' : convert_text_to_datefield(pubDate),
            'duration' : duration,
            'audio_file' : audio_file,
            'image' : image,
            'explicit' : convert_text_to_boolianfield(explicit),
        }
    ) 
        
    
    # item = Episode.objects.create(
        
    #     title = [elm.text for elm in root.findall(".//item/title", itunes_namespace)],
    #     # print(title)
    #     subtitle = [elm.text for elm in root.findall(".//item/itunes:subtitle", itunes_namespace)],
    #     # print(subtitle)
    #     description = [elm.text for elm in root.findall(".//item/description", itunes_namespace)],
    #     # print(description)
        
    #     pubDate = [elm.text for elm in root.findall(".//item/pubDate", itunes_namespace)],
    #     # print(pubDate)
    #     image = [elm.attrib for elm in root.findall(".//item/itunes:image", itunes_namespace)],
    #     # print(image)
    #     audio_file = [elm.attrib for elm in root.findall(".//item/enclosure", itunes_namespace)],
    #     # print(audio_file)
    #     guid = [elm.text for elm in root.findall(".//item/guid", itunes_namespace)],
    #     # print(guid)
    #     duration = [elm.text for elm in root.findall(".//item/itunes:duration", itunes_namespace)],
    #     # print(duration)
    #     explicit = [elm.text for elm in root.findall(".//item/itunes:explicit", itunes_namespace)],
    #     # print(explicit)
    
    # )
    
    
    # return {
    #         'title': title,
    #         'subtitle': subtitle,
    #         'description' : description,
    #         'guid' : guid,
    #         'pubDate' : pubDate,
    #         'duration' : duration,
    #         'audio_file' : audio_file,
    #         'image' : image,
    #         'explicit' : explicit,
    #     }
    
 


# print(channel_parser())
# print(item_parser())

# channel_parser()
# item_parser()