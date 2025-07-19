from rest_framework import serializers
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
import re

class FilesSerializer(serializers.Serializer):
    knowledge_db_name = serializers.CharField(
        required=True,
        help_text="知识库名称"
    )
    embedding = serializers.CharField(
        max_length=10,
        min_length=1,
        help_text="embedding,长度1-10个字符"
    )

    files = serializers.ListField(
        child=serializers.CharField(
            max_length=256,
            min_length=1,
        ),
        help_text="文件列表"
    )
    
    def validate_embedding(self, value):
        return value.strip()
    
    def validate(self, attrs): 
        return attrs 