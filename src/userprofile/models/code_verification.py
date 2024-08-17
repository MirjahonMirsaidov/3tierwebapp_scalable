from django.db import models

from core.utils.base_model import BaseModel


class CodeVerification(BaseModel):
    email = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=255, null=True)
    code = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Code Verification'
        verbose_name_plural = 'Code Verifications'
        db_table = 'code_verification'
