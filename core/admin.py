from django.contrib import admin
from .models import Channel, Episode, News, Category, XmlLink, News, Type
# Register your models here.
admin.site.register(Channel)
admin.site.register(Episode)
admin.site.register(Category)
admin.site.register(XmlLink)
admin.site.register(News)
admin.site.register(Type)