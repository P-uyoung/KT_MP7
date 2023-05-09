from django.db import models

# Create your models here.

class ChatResult(models.Model):
    prompt = models.CharField(max_length=1000)
    content = models.TextField()
    pub_date = models.DateTimeField('date published')