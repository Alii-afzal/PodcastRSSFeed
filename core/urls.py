from django.urls import path
from .views import ExtractXML
 
 
urlpatterns = [
    path('extracts/', ExtractXML.as_view()) 
]
