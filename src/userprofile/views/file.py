from django.core.cache import cache
from rest_framework.generics import CreateAPIView, ListAPIView

from userprofile.models import FileUpload
from userprofile.serializers.file_upload import FileUploadSerializer, FileListSerializer


class FileUploadGenericView(CreateAPIView):
    serializer_class = FileUploadSerializer

    def perform_create(self, serializer):
        s = serializer.save(user=self.request.user)
        files = cache.get("files_queryset")
        print(files)
        return s


class FileListGenericView(ListAPIView):
    serializer_class = FileListSerializer

    def get_queryset(self):
        files = cache.get("files_queryset")
        print(files)
        if not files:
            files = FileUpload.objects.all()
            cache.set("files_queryset", files, 300)
            print("Cache miss")
        else:
            print("Cache hit")
        return FileUpload.objects.all()
