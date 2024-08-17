from rest_framework import serializers

from core.utils.aws import cdn_client
from userprofile.models import FileUpload


class FileUploadSerializer(serializers.ModelSerializer):
    file = serializers.FileField(max_length=None, write_only=True)

    class Meta:
        model = FileUpload
        fields = (
            "file",
            "file_path",
            "description",
        )
        extra_kwargs = {
            "file_path": {"read_only": True},
        }

    def create(self, validated_data):
        file = validated_data.pop("file")
        file_path = cdn_client.upload_file(file.name, file)
        instance = FileUpload.objects.create(file_path=file_path, **validated_data)
        return instance


class FileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = (
            "id",
            "file_path",
            "description",
        )

