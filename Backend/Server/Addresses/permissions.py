from rest_framework.permissions import BasePermission, SAFE_METHODS



class CityProvinceAdminPermission(BasePermission):
    """
    Custom permission for the City and Province models.

    - Only admin users (i.e. request.user.is_staff == True) are allowed to create, update, or delete objects.
    - All safe methods (GET, HEAD, OPTIONS) are allowed for everyone.
    """
    
    def has_permission(self, request, view):
        # Allow read-only actions for everyone.
        if request.method in SAFE_METHODS:
            return True
        # All write operations (create, update, delete) require admin privileges.
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # Allow safe methods.
        if request.method in SAFE_METHODS:
            return True
        # For object-level write operations, only admin users are allowed.
        return request.user and request.user.is_staff



class RecipientAddressPermission(BasePermission):
    """
    Custom permission for RecipientAddress:

    - Safe methods (GET, HEAD, OPTIONS) are allowed for everyone.
    - For creation (POST), update (PUT/PATCH), and other modifying actions, only admin users
      (i.e. request.user.is_staff == True) or users with a user_type of "SC" are allowed.
    """
    
    def has_permission(self, request, view):
        # Allow safe methods for any request.
        if request.method in SAFE_METHODS:
            return True
        
        # For modifying endpoints check if the user is admin or SC user.
        return request.user and (request.user.is_staff or getattr(request.user, 'user_type', None) == "SC")
    
    def has_object_permission(self, request, view, obj):
        
        if obj.recipient == request.user:
            return True
