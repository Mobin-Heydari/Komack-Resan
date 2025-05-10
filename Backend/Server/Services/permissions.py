from rest_framework.permissions import BasePermission, SAFE_METHODS



class IsServiceActionAllowed(BasePermission):
    """
    Custom permission for the Service resource.
    
    - For creation (POST): Only a user whose user_type equals "SC" (service recipient) is allowed.
    - For update/delete (PUT/PATCH/DELETE): Only a user whose user_type equals "AD" (admin),
      or the Service's recipient, or the Service's provider is allowed.
    - All safe methods are allowed for everyone.
    """
    
    def has_permission(self, request, view):
        # Allow all safe methods.
        if request.method in SAFE_METHODS:
            return True
        
        # For creation, only allow if the user's type is "SC".
        if request.method == "POST":
            return getattr(request.user, 'user_type', None) == "SC"
        
        # For other actions, we defer to object-level permission checks.
        return True

    def has_object_permission(self, request, view, obj):
        # Allow safe methods.
        if request.method in SAFE_METHODS:
            return True
        
        # Allow if the user is an admin (user_type "AD").
        if getattr(request.user, 'user_type', None) == "AD":
            return True
        
        # Allow if the user is the Service's recipient.
        if obj.recepient == request.user:
            return True
        
        # Allow if the user is the Service's provider.
        if obj.service_provider == request.user:
            return True
        
        return False
