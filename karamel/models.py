from django.db import models
from validate.models import UserInfo

# Create your models here.
class Blogdetails(models.Model):
    userinfo = models.ForeignKey(UserInfo ,on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    description = models.TextField()
    blogpic = models.ImageField(upload_to = "blogs")
    blogref = models.TextField()