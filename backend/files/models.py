from django.db import models

# Create your models here.
class File(models.Model):
    knowledge_db_name = models.CharField(max_length=255)
    files = models.JSONField(default=list)
    embedding = models.CharField(max_length=64)