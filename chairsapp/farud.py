from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os

class FraudDetectionController(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):

        file = request.FILES['file']
        file_name = file.name
        file_path = os.path.join('images', file_name)
        path = default_storage.save(file_path, ContentFile(file.read()))

        full_path = default_storage.path(path)
        return Response({"file_path": full_path}, status=status.HTTP_201_CREATED)