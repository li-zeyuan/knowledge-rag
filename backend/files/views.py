from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .serializers import CreateFileSerializer, GetPreSignedUrlSerializer
from plugins.chroma import create_db, get_knowledge_db_list, delete_db
from plugins.minio import gen_presigned_put_url
from rest_framework.decorators import action
class FilesView(viewsets.ViewSet):
    @action(detail=False, methods=['post'], url_path='presigned_put')
    def presigned_put(self, request):
        ser = GetPreSignedUrlSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

        file_name = ser.validated_data.get('file_name', '')
        return Response({"url": gen_presigned_put_url(file_name)}, status=status.HTTP_200_OK)
    
    def create(self, request):
        fileSerializer = CreateFileSerializer(data=request.data)
        if not fileSerializer.is_valid():
            return Response(fileSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

        knowledge_db_name = fileSerializer.validated_data.get('knowledge_db_name', '')
        file_name = fileSerializer.validated_data.get('file_name', '')
        embedding = fileSerializer.validated_data.get('embedding', '')

        create_db(knowledge_db_name, file_name, embedding) 
        return Response({}, status=status.HTTP_200_OK)

    def list(self, request):
        list = get_knowledge_db_list()
        return Response(list, status=status.HTTP_200_OK)

    @action(detail=False, methods=['delete'], url_path='del')
    def del_db(self, request):
        knowledge_db_name = request.data.get('knowledge_db_name', '')
        delete_db(knowledge_db_name)
        return Response("ok", status=status.HTTP_200_OK)