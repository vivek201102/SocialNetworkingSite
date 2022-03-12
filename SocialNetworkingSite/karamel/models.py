from tkinter import CASCADE
from urllib import request
from django.db import models
from validate.models import UserInfo

# Create your models here.
class Blogdetails(models.Model):
    userinfo = models.ForeignKey(UserInfo ,on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    description = models.TextField()
    blogpic = models.ImageField(upload_to = "blogs")
    blogref = models.TextField()
    dandt = models.CharField(max_length=25, default="none")


class Friend(models.Model):
    userinfo = models.ForeignKey(UserInfo,on_delete=models.CASCADE)
    fromuser = models.CharField(max_length=255)
    touser = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="requested")