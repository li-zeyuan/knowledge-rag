from django.shortcuts import render

from rest_framework import viewsets
from .models import Models
from .serializers import ModelsSerializer

# Create your views here.
class ModelsView(viewsets.ModelViewSet):
    queryset = Models.objects.all()  # type: ignore
    serializer_class = ModelsSerializer