from django.db import models

from core.utils.base_model import BaseModel


class Role(BaseModel):
    name = models.CharField(max_length=150, unique=True)
    name_ru = models.CharField(max_length=150)
    name_uz = models.CharField(max_length=150)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = "Role"
        verbose_name_plural = "Roles"
        db_table = "role"


class RolePermission(BaseModel):
    role = models.ForeignKey('userprofile.Role', null=True, on_delete=models.SET_NULL)
    key = models.CharField(max_length=150)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = "Role Permission"
        verbose_name_plural = "Role Permissions"
        db_table = "role_permission"
