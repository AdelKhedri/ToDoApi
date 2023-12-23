from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    invaited_by = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.username


# 