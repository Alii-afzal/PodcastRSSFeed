from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from accounts.managers import UserManager

class User(AbstractBaseUser):
    email = models.EmailField(max_length=25, unique=True)
    phone_number =models.CharField(max_length=11, unique=True)
    full_name = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'full_name']
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin
    

class NotificationInfo(models.Model):
    message = models.TextField()
    
    def __str__(self):
        return self.message
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(NotificationInfo, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.message}"
    