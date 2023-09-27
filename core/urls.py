from django.urls import path
from core.views import ExtractXML
 
 
urlpatterns = [
    path('extracts/', ExtractXML.as_view()) 
]
