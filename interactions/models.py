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
    
