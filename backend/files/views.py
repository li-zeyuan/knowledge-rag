from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .serializers import FilesSerializer

class FilesView(viewsets.ViewSet):
    def create(self, request):
        fileSerializer = FilesSerializer(data=request.data)
        if not fileSerializer.is_valid():
            return Response(fileSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # todo 写入向量数据库
        return Response('create ok', status=status.HTTP_200_OK)