from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admins to edit it.
    """
    def has_object_permission(self, request, view, obj):
        
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user or request.user.is_staff