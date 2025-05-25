from rest_framework.permissions import BasePermission, SAFE_METHODS
from Services.models import Service




class ServiceScorePermission(BasePermission):
    """
    Custom permission for ServiceScore operations.
    
    - For creation (POST): Only a service recipient (user_type "SC") or an admin (user_type "AD") 
      can create a score. Additionally, if the user is a service recipient, the Service identified 
      by 'service_slug' in the request must have its recipient equal to the currently authenticated user.
    
    - For update (PUT/PATCH): Only an admin (user_type "AD") or the Service's recipient can update 
      the score.
    
    - Safe methods (GET, HEAD, OPTIONS) are always allowed.
    """
    
    def has_permission(self, request, view):
        # Allow safe methods.
        if request.method in SAFE_METHODS:
            return True

        # For create operation: allow if the user is a service recipient (SC) or an admin (AD).
        if request.method == "POST":
            # Correctly check if the user's type is either SC or AD.
            if getattr(request.user, 'user_type', None) not in ["SC", "AD"]:
                return False

            # service_slug must be provided.
            service_slug = request.data.get("service_slug")
            if not service_slug:
                return False  
            
            # Look up the Service using the provided slug.
            try:
                service = Service.objects.get(slug=service_slug)
            except Service.DoesNotExist:
                return False
            
            # If the user is a service recipient, ensure the service's recipient matches the user.
            if request.user.user_type == "SC" and service.recipient != request.user:
                return False
            
            return True

        # For update or other non-POST methods, defer object-level checks to has_object_permission.
        return True

    def has_object_permission(self, request, view, obj):
        # Allow safe methods.
        if request.method in SAFE_METHODS:
            return True

        # For update: allow if user is admin.
        if getattr(request.user, 'user_type', None) not in ["AD", "SC"]:
            return True
        
        # Allow update if the service's recipient matches the requesting user.
        if obj.service.recipient == request.user:
            return True
        
        return False
