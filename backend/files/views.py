from django.db import transaction
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .serializers import CreateFileSerializer, GetPreSignedUrlSerializer
from plugins.chroma import create_db, get_knowledge_db_list, delete_db
from plugins.minio import gen_presigned_put_url
from rest_framework.decorators import action
from .models import File

class FilesView(viewsets.ViewSet):
    @action(detail=False, methods=['post'], url_path='presigned_put')
    def presigned_put(self, request):
        ser = GetPreSignedUrlSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

        file_name = ser.validated_data.get('file_name', '')
        url, key = gen_presigned_put_url(file_name)
        return Response({"url": url, "key": key}, status=status.HTTP_200_OK)
    
    def create(self, request):
        fileSerializer = CreateFileSerializer(data=request.data)
        if not fileSerializer.is_valid():
            return Response(fileSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

        knowledge_db_name = fileSerializer.validated_data.get('knowledge_db_name', '')
        files = fileSerializer.validated_data.get('files', [])
        embedding = fileSerializer.validated_data.get('embedding', '')

        with transaction.atomic():
            instance = File(knowledge_db_name=knowledge_db_name, files=files, embedding=embedding)
            instance.save()

            create_db(instance.id, files, embedding) 

        return Response({"id": instance.id}, status=status.HTTP_200_OK)

    def list(self, request):
        files = File.objects.all().order_by('-id')
        names = [file.knowledge_db_name for file in files]
        return Response({"names": names}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['delete'], url_path='del')
    def del_db(self, request):
        knowledge_db_name = request.data.get('knowledge_db_name', '')
        delete_db(knowledge_db_name)
        return Response("ok", status=status.HTTP_200_OK)