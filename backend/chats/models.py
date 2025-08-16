from django.db import models

# Create your models here.

ChatTypeChatLLM = 1
ChatTypeChatKnowledgeWithHistory = 2
ChatTypeChatKnowledgeWithoutHistory = 3

class Chat(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    uid = models.IntegerField(default=0)
    prompt = models.TextField()
    bot_message = models.TextField()
    is_error = models.BooleanField(default=False)
    chat_type = models.CharField(max_length=255)
    llm = models.CharField(max_length=255)
