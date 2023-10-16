from django.urls import path
from .views import ExtractXMLChannel, ExtractXMLItems
 
 
urlpatterns = [
    path('extractchannel/', ExtractXMLChannel.as_view()),
    path('extractitem/', ExtractXMLItems.as_view()),
    # path('update_episode/', UpdateEpisodesView.as_view()),
    # path('test/', TestView.as_view()),
]
