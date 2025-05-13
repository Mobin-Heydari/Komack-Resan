from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsInvoiceAdmin(BasePermission):
    """
    Custom permission for Invoice-related objects.

    - For safe methods (GET, HEAD, OPTIONS): allow access to everyone.
    - For write operations (POST, PUT, PATCH, DELETE): only allow if the request user is admin (is_staff == True).
    """
    
    def has_permission(self, request, view):
        # Allow safe methods for everyone.
        if request.method in SAFE_METHODS:
            return True
        # Otherwise check that the user is authenticated and is an admin.
        return request.user and request.user.is_authenticated and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # Allow safe methods for everyone.
        if request.method in SAFE_METHODS:
            return True
        # For object-level operations restrict to admin users.
        return request.user and request.user.is_authenticated and request.user.is_staff
