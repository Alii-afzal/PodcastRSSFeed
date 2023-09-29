from django.db import models
from core.models import Channel, Episode
from accounts.models import User

# Create your models here.
class Subscribe(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    
class Like(models.Model):
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    channel = models.OneToOneField(Channel, on_delete=models.CASCADE)
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE)
    create_at = models.DateTimeField()