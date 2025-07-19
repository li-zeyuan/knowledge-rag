from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .serializers import FilesSerializer
from database.database import create_db, get_knowledge_db_list, delete_db
from rest_framework.decorators import action
class FilesView(viewsets.ViewSet):
    def create(self, request):
        fileSerializer = FilesSerializer(data=request.data)
        if not fileSerializer.is_valid():
            return Response(fileSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

        knowledge_db_name = fileSerializer.validated_data.get('knowledge_db_name', '')
        files = fileSerializer.validated_data.get('files', [])
        embedding = fileSerializer.validated_data.get('embedding', '')

        create_db(knowledge_db_name, files, embedding) 
        return Response({}, status=status.HTTP_200_OK)

    def list(self, request):
        list = get_knowledge_db_list()
        return Response(list, status=status.HTTP_200_OK)

    @action(detail=False, methods=['delete'], url_path='del')
    def del_db(self, request):
        knowledge_db_name = request.data.get('knowledge_db_name', '')
        delete_db(knowledge_db_name)
        return Response("ok", status=status.HTTP_200_OK)