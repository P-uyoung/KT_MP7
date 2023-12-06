from django.db import models

# Create your models here.
class ChatHistory(models.Model):
    session_id = models.CharField(max_length=255)
    user_message = models.TextField()
    gpt_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # 정렬에 필요