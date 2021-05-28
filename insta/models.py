from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class Posts(models.Model):
    owner = models.CharField(max_length = 20)
    image = models.URLField(null=True, max_length = 100000)
    caption = models.CharField(null=True, max_length = 100)
    likes = models.IntegerField(default=0)

class Comments(models.Model):
    comment = models.CharField(max_length = 100)
    commenter = models.CharField(max_length = 20)
    post = models.IntegerField()

class Saved(models.Model):
    users = models.IntegerField()
    post = models.IntegerField()