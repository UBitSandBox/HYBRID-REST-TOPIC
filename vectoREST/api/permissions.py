from rest_framework.permissions import BasePermission


class ConfigRight(BasePermission):
    """
    Right for endpoint /config
    """
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name='config'):
            return True
        return False


class VectorsRight(BasePermission):
    """
    Right for endpoint /vectors
    """
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name='vectors'):
            return True
        return False