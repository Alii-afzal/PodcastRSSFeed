from rest_framework import serializers
from rssfeedparser.models import Channel, Episode, News,  XmlLink

class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = [
            'title',
            'subtitle',
            'description',
            'pubDate',
            'image',
            'language',
            'author',
            'source',
            'owner',
        ]
    
        
class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = [
            'title',
            'subtitle',
            'description',
            'guid',
            'pub_date',
            'duration',
            'audio_file',
            'image',
            'explicit',
        ]
        
        # depth = 2
    