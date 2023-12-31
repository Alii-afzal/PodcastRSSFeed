from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from core.models import Channel, Episode, Category
from accounts.models import User


class Subscribe(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user} subscribe {self.channel}"

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
    
class BookMark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.episode} Bookmarked by {self.user}"
    
# class Recommendation(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
#                              related_name='category_recommendations')
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     count = models.PositiveIntegerField(default=0)

#     def __str__(self):
#         return f'{self.user.username} interest in: {self.category.name}'

    # class Meta:
    #     ordering = ['-count']