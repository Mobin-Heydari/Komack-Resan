from rest_framework.permissions import BasePermission, SAFE_METHODS



class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission that allows only admin users to create, update, or delete items.
    Read operations (GET, HEAD, OPTIONS) are permitted for all users.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True  # Allow read actions for everyone
        return request.user and request.user.is_authenticated and request.user.is_staff