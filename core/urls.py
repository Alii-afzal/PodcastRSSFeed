from django.urls import path
from rssfeedparser.views import ExtractXML
 
 
urlpatterns = [
    path('extracts/', ExtractXML.as_view()) 
]
