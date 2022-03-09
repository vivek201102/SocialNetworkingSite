from datetime import datetime
from email import message
from django.db import models

# Create your models here.
class friendchatpage(models.Model):
    fromuser = models.CharField(max_length=25, null=False)
    touser = models.CharField(max_length=25, null=False)
    url = models.CharField(max_length=255, null=False, unique=True)
    status = models.CharField(max_length=25, default="Active")



class friendmessage(models.Model):
    date = models.CharField(max_length=25, default=datetime.now().strftime("%I:%M%p"))
    message = models.TextField()
    touser = models.CharField(max_length=25, null=False)
    fromuser = models.CharField(max_length=25, null=False)
    url = models.CharField(max_length=255, null=False)
    