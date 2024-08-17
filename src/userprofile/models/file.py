from django.db import models

from core.utils.base_model import BaseModel


class FileUpload(BaseModel):
    """ Profile (custom User ) model """
    file_path = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=255, null=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = "FileUpload"
        verbose_name_plural = "FileUploads"
        db_table = "file"




