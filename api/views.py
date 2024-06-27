import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.text import get_valid_filename
from django.views import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.functions import start_process


# Create your views here.
class DenoiserAPIView(APIView):
    def post(self, request, *args, **kwargs):

        if 'audio_file' not in request.FILES:
            return Response({"error": "No audio file provided"}, status=status.HTTP_400_BAD_REQUEST)
        audio_file = request.FILES['audio_file']

        filename = get_valid_filename(audio_file.name)
        inputs_dir = os.path.join(settings.MEDIA_ROOT, 'inputs')
        os.makedirs(inputs_dir, exist_ok=True)

        fs = FileSystemStorage(location=inputs_dir)
        saved_file = fs.save(filename, audio_file)
        file_path = os.path.join('inputs', saved_file)
        file_url = fs.url(file_path)

        target_file,  source_graph, target_graph = start_process(file_path)

        target_file = os.path.basename(target_file)
        target_graph = os.path.basename(target_graph)
        source_graph = os.path.basename(source_graph)

        return JsonResponse({'Source_path': file_url, 'Target_path': "/media/outputs/" + target_file, 'Target_graph': "/media/graphs/" + target_graph, 'original_graph': "/media/graphs/" + source_graph}, status=status.HTTP_201_CREATED)

class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')