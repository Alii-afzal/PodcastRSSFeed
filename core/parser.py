from datetime import datetime
import requests
import xml.etree.ElementTree as ET
from .models import Channel, Episode, Category


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

        print(owner)
    
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
    response = requests.get('https://rss.art19.com/apology-line')
    xml_data = response.text
    root = ET.fromstring(xml_data)
    itunes_namespace = {'itunes':'http://www.itunes.com/dtds/podcast-1.0.dtd'}
    
    title = [elm.text for elm in root.findall(".//item/title", itunes_namespace)],
    # print(title)
    titles=[]
    for elm in root.findall(".//item", itunes_namespace):
        if elm.findall('.//title'):
            title = elm.find('.//title').text
        else:
            title = None
        titles.append(title)
        print(title)
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
        
    # item = Episode.objects.create(
    #     **{
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
    # ) 
    for title in titles:
        Episode.objects.create(title=title)
    
# channel_parser()
# item_parser()

# import requests
# import xml.etree.ElementTree as ET
# from your_app.models import Episode  # Replace 'your_app' with the actual name of your Django app

# def item_parser():
#     response = requests.get('https://rss.art19.com/apology-line')
#     xml_data = response.text
#     root = ET.fromstring(xml_data)
#     itunes_namespace = {'itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd'}
    
#     # Create a list to store all the titles
#     titles = []

#     for elm in root.findall(".//item", itunes_namespace):
#         if elm.findall('.//title'):
#             title = elm.find('.//title').text
#         else:
#             title = None
        
#         # Append the title to the titles list
#         titles.append(title)

#     # Create Episode objects using the titles
#     for title in titles:
#         Episode.objects.create(title=title)






