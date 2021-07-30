from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    允许所有者访问
    """
    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        else:
            raise PermissionDenied('非所有者，不可访问')
