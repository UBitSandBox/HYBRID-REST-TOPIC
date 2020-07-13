from rest_framework.permissions import BasePermission


class ConfigRight(BasePermission):
    """Right for endpoint /config"""
    def has_permission(self, request, view):
        return bool(request.user and request.user.groups.filter(name='config'))


class VectorsRight(BasePermission):
    """Right for endpoint /vectors"""
    def has_permission(self, request, view):
        return bool(request.user and request.user.groups.filter(name='vectors'))
