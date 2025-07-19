from rest_framework.response import Response
from rest_framework import viewsets
from application.settings import LLM_MODELS, EMBEDDING_MODELS
from rest_framework.decorators import action
# Create your views here.
class ModelsView(viewsets.ModelViewSet):
    @action(detail=False, methods=['get'], url_path='llm_models')
    def llm_models(self, request):
        return Response(LLM_MODELS)
    
    @action(detail=False, methods=['get'], url_path='embedding_models')
    def embedding_models(self, request):
        return Response(EMBEDDING_MODELS)