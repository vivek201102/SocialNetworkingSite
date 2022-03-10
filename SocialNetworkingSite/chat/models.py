from datetime import datetime
from email import message
from django.db import models

# Create your models here.

class friendmessage(models.Model):
    date = models.CharField(max_length=25, default=datetime.now().strftime("%I:%M%p"))
    message = models.TextField()
    touser = models.CharField(max_length=25, null=False)
    fromuser = models.CharField(max_length=25, null=False)
    