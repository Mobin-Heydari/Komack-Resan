from rest_framework.permissions import BasePermission

class IsInvoiceAdmin(BasePermission):
    """
    Custom permission to only allow admin users to access or modify Invoice objects.
    
    Only a user with an admin flag (e.g., is_staff == True) will have both global
    and object-level permission.
    """

    def has_permission(self, request, view):
        # Globally, only allow requests if the user is an admin.
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # Object-level permission: only allow if the user is an admin.
        return request.user and request.user.is_staff
