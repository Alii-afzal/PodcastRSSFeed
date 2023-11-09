from rest_framework import serializers
from .models import Channel, Episode, News,  XmlLink


class XmlLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = XmlLink
        # fields = ('id', 'url')
        fields = "__all__"
class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields="__all__"
        # fields = [
        #     'title',
        #     'subtitle',
        #     'description',
        #     'pubDate',
        #     'image',
        #     'language',
        #     'author',
        #     'source',
        #     'owner',
        # ]
    
        
class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = "__all__"
        # fields = [
        #     'title',
        #     'subtitle',
        #     'description',
        #     'guid',
        #     'pubDate',
        #     'duration',
        #     'audio_file',
        #     'image',
        #     'explicit',
        # ]
        
        # depth = 2
    