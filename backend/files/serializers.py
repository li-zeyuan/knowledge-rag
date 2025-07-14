from rest_framework import serializers
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
import re

class FilesSerializer(serializers.Serializer):
    name = serializers.CharField(
        max_length=100,
        min_length=1,
        help_text="文件名,长度1-100个字符"
    )
    
    def validate_name(self, value):
        print(f"validate_name: {value}")

        return value.strip()
    
    def validate(self, attrs):
        if not attrs.get('name'):
            raise serializers.ValidationError("文件名不能为空")
        
        return attrs 