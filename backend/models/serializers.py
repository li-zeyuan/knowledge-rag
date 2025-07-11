from rest_framework import serializers

from models.models import Models

class ModelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Models
        fields = '__all__'