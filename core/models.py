from django.db import models

class Type(models.Model):
    pass

class Category(models.Model):
    title = models.CharField(max_length=50)
    
    def __str__(self):
        return self.title
    

class XmlLink(models.Model):
    xml_link = models.URLField(unique=True)
    rss_type = models.ForeignKey(Type, on_delete=models.PROTECT)

class Channel(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    subtitle = models.CharField(max_length=30, blank=True, null=True)
    language = models.CharField(max_length=30, blank=True, null=True)
    pubDate = models.DateTimeField(blank=True, null=True)
    duration = models.CharField(max_length=50 , blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    image = models.URLField(blank=True, null=True)
    owner = models.CharField(max_length=50, blank=True, null=True)
    author = models.TextField(blank=True, null=True)
    source = models.URLField(blank=True, null=True)
    xml_link = models.URLField()
    
    def __str__(self):
        return self.title
    

class Episode(models.Model):
    title = models.CharField(max_length=30)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, null=True, blank=True)
    subtitle = models.CharField(max_length=30, blank=True, null=True)
    guid = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    pubDate = models.DateTimeField(blank=True, null=True)
    duration = models.CharField(max_length=50, blank=True, null=True)
    audio_file = models.URLField()
    image = models.URLField(blank=True, null=True)
    explicit = models.BooleanField(blank=True, null=True)

    
    def __str__(self):
        return self.title
    
class News(models.Model):
    title = models.CharField(max_length=50)
    channel =models.ForeignKey(Channel, on_delete=models.CASCADE)
    guid = models.CharField(max_length=200)
    pubDate = models.DateTimeField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    source = models.URLField(blank=True, null=True)
    
    
    def __str__(self):
        return self.title
    