from django.shortcuts import render
# from RSSfeed.parsers import PodcastParser, Parser, xml_data
from rest_framework import status
from rest_framework.views import APIView
from .serializers import ChannelSerializer, EpisodeSerializer, XmlLinkSerializer
from rest_framework.response import Response
from .models import Episode, Channel, XmlLink
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from accounts.authentication import JWTAuthentication
from core.tasks import update_all_podcasts, update_podcast
# from .parser import xml_parser
# from django.utils.translation import gettext_lazy as _
from core.parser import XMLParser

class ExtractXMLChannel(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes=[IsAdminUser]
    
    def get(self, request):
        parsed_data = Channel.objects.all()
        ser_data = ChannelSerializer(instance=parsed_data, many=True)
        return Response(data=ser_data.data)
    
class ExtractXMLItems(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes=[IsAdminUser]
    
    def get(self, request):
        parsed_data = Episode.objects.all()
        ser_data = EpisodeSerializer(instance=parsed_data, many=True)
        return Response(data=ser_data.data)
    
class UpdateEpisodesView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes=[IsAdminUser]
    
    def get(self, request):
        xml_parser = XMLParser(request.data.get('xml_link'))
        xml_parser.update_episodes()  
        return Response({"message": ("Episodes updated successfully")}, status=status.HTTP_200_OK)


class AddPodcastUrlView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes=[IsAdminUser]

    def post(self,request):
        serializer = XmlLinkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response( ("URL is saved"), status=status.HTTP_201_CREATED)
    
class AddPodcastAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes=[IsAdminUser]

    def post(self, request):
        parser = XMLParser(request.data.get('xml_link'))
        data = parser.xml_link_parse()
        print(data)
        if not data:
            raise Response(_('URL is invalid!'), status=status.HTTP_400_BAD_REQUEST)
        
        parser.seve_channel_in_database(data)
        return Response({"message":("Rss file save in database successfully.")}, status.HTTP_201_CREATED)
    
class UpdatePodcastTaskAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        # data = None
        # print(data)
        # if data:
            update_all_podcasts.delay()
            return Response({"message":("All urls are going to update")}, status.HTTP_201_CREATED)
            # raise Response(_('xml is invalid!'), status=status.HTTP_400_BAD_REQUEST)
        # update_podcast.delay(data)
        # return Response({"message":_("xml is going to update")}, status.HTTP_201_CREATED)