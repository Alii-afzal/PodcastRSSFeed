from django.shortcuts import render
# from RSSfeed.parsers import PodcastParser, Parser, xml_data
from rest_framework.views import APIView
from .serializers import ChannelSerializer, EpisodeSerializer
from rest_framework.response import Response
from .models import Episode, Channel
from .parser import XMLParser

class ExtractXMLChannel(APIView):
    def get(self, request):
        parsed_data = Channel.objects.all()
        ser_data = ChannelSerializer(instance=parsed_data, many=True)
        return Response(data=ser_data.data)
    
class ExtractXMLItems(APIView):
    def get(self, request):
        parsed_data = Episode.objects.all()
        ser_data = EpisodeSerializer(instance=parsed_data, many=True)
        return Response(data=ser_data.data)