from rest_framework import permissions


class IsRole(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            return request.user.role.name == 'role_name'
        except:
            return False



