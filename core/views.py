from django.shortcuts import render
# from RSSfeed.parsers import PodcastParser, Parser, xml_data
from rest_framework import status
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
    
class UpdateEpisodesView(APIView):
    def get(self, request):
        xml_parser = XMLParser()  # Create an instance of your XMLParser
        try:
            xml_parser.update_episodes()  # Call the update_episodes method
            return Response({"message": "Episodes updated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)