from rest_framework.permissions import BasePermission, SAFE_METHODS
from Services.models import Service



class ServiceScorePermission(BasePermission):
    """
    Custom permission for ServiceScore operations.
    
    - For creation (POST): Only a service recipient (user_type "SC") can create a score,
      and the Service identified by 'service_slug' in the request must have its recepient
      equal to the currently authenticated user.
    
    - For update (PUT/PATCH): Only an admin (user_type "AD") or the Service's recipient can update 
      the score.
    
    - Safe methods are always allowed.
    """
    
    def has_permission(self, request, view):
        # Allow safe methods.
        if request.method in SAFE_METHODS:
            return True

        # For create operation: Only allow if the user is a Service Recipient.
        if request.method == "POST":
            if getattr(request.user, 'user_type', None) != "SC":
                return False

            service_slug = request.data.get("service_slug")
            if not service_slug:
                return False  # A service_slug is required.
            
            # Look up the Service using the provided slug.
            try:
                service = Service.objects.get(slug=service_slug)
            except Service.DoesNotExist:
                return False
            
            # Only allow creation if the service's recipient matches the requesting user.
            if service.recipient != request.user:
                return False
            return True
        
        # For update operations, defer object-level checks to has_object_permission.
        return True

    def has_object_permission(self, request, view, obj):
        # Allow safe methods.
        if request.method in SAFE_METHODS:
            return True
        
        # For update: allow if user is admin OR if the service's recipient matches the requesting user.
        if getattr(request.user, 'user_type', None) == "AD":
            return True
        if obj.service.recepient == request.user:
            return True
        
        return False
