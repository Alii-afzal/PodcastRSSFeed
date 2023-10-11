from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from core.models import Channel, Episode
from accounts.models import User


class Subscribe(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user} subscribe {self.channel}"
    


# class Subscribe(models.Model):
#     user =  models.ForeignKey(User, on_delete=models.CASCADE)
    
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey('content_type', 'object_id')
    
# class Like(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
    
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey('content_type', 'object_id')

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user} liked {self.episode}"
    
    

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=False, null=False)
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user} write comment for {self.episode}"
    
    
# class Comment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     content = models.TextField(blank=False, null=False)
    
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey('content_type', 'object_id')

  

class BookMark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.episode} Bookmarked by {self.user}"
  
# class Bookmark(models.Model):
#     user=models.ForeignKey(User, on_delete=models.CASCADE)
    
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey('content_type', 'object_id')