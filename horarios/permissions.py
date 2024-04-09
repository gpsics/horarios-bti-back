from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admin users to edit objects.
    """

    def has_permission(self, request, view):
        # Permite a leitura de todos
        if request.method in permissions.SAFE_METHODS:
            return True

        # Permite a edição apenas para administradores
        return request.user and request.user.is_staff