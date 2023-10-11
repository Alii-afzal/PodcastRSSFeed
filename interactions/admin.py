from django.contrib import admin
from .models import Like, Comment, Subscribe, BookMark

# Register your models here.
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Subscribe)
admin.site.register(BookMark)