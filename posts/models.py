from django.db import models
from django.db.models.base import Model
from users.models import *

# Create your models hereu.


class SocailPosts(models.Model):
    post_title = models.CharField(max_length=100, blank=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)


class Images(models.Model):
    post = models.ForeignKey(SocailPosts, on_delete=models.CASCADE,null=True,blank=True)
    image = models.FileField(blank=True)
    description = models.TextField(null=True,blank=True)
    tags = models.CharField(max_length=50,null=True,blank=True)

class LikeDislike(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(SocailPosts,on_delete=models.CASCADE)
    like = models.BooleanField(null=False,blank=False)