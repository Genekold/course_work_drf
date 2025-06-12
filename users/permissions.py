from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Проверка является ли пользователь Владельцем"""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
