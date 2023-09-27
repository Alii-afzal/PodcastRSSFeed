from django.shortcuts import render
# from RSSfeed.parsers import PodcastParser, Parser, xml_data
from rest_framework.views import APIView
from rssfeedparser.serializers import ChannelSerializer, EpisodeSerializer
from rest_framework.response import Response
from rssfeedparser.models import Episode, Channel
from .parser import channel_parser, item_parser
class ExtractXML(APIView):
    def get(self, request):
        channel_parser()
        parsed_data = Channel.objects.all()
        ser_data = EpisodeSerializer(instance=parsed_data, many=True)
        return Response(data=ser_data.data)
    
    # def get(self, request):
    #     parsed_data = Episode.objects.all()
    #     ser_data = ChannelSerializer(instance=parsed_data, many=True)
    #     return Response(data=ser_data.data)
    
    # def get(self, request): 
    #     articles = Episode.objects.all()
    #     serializer = EpisodeSerializer(articles, many=True)
    #     return Response(serializer.data)
    # def post(self, request):
    #     serializer = EpisodeSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         parsed_data = PodcastParser(xml_data).parse_xmls()
    #         for item in parsed_data :
    #             item.save()
    #         articles = Episode.objects.all()
    #         serializer = EpisodeSerializer(articles, many=True)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
