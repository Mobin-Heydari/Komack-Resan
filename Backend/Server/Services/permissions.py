from rest_framework.permissions import BasePermission, SAFE_METHODS

from Companies.models import CompanyAccountant, CompanyExpert, CompanyReceptionist



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
            return getattr(request.user, 'user_type', None) == "SC" or "AD"
        
        # For other actions, we defer to object-level permission checks.
        return True

    def has_object_permission(self, request, view, obj):
        # Allow safe methods.
        if request.method in SAFE_METHODS:
            return True
        
        # Allow if the user is an admin (user_type "AD").
        if request.user.is_staff:
            return True
        
        # Allow if the user is the Service's recipient.
        if obj.recipient == request.user:
            return True
        
        if obj.accountant.employee == request.user:
            return True
        
        if obj.expert.employee == request.user:
            return True
        
        if obj.receptionist.employee == request.user:
            return True
        
        return False


class IsServicePaymentActionAllowed(BasePermission):
    """
    Custom permission for the ServicePayment resource.
    
    - For safe methods (GET, HEAD, OPTIONS): Allow all.
    
    - For creation (POST): Allow only if the current user's type is "SC" (service recipient) 
      or if the user is an admin (user_type "AD").
    
    - For update/delete (PUT/PATCH/DELETE): Allow if the user is an admin,
      or if the user is the Service's recipient,
      or if a CompanyAccountant record exists for the service's company with the current user as the employee.
    """

    def has_permission(self, request, view):
        # Allow safe methods for everyone.
        if request.method in SAFE_METHODS:
            return True
        
        # For other methods (update/delete), return True here; object-level checks are applied later.
        return True

    def has_object_permission(self, request, view, obj):
        # Allow safe methods.
        if request.method in SAFE_METHODS:
            return True

        # Admin users are allowed.
        if request.user.is_staff:
            return True
        
        # Allow if the current user is the Service's recipient.
        if obj.service.recipient == request.user:
            return True
        
        # Allow if the current user is registered as an accountant for the Service's company.
        if obj.service.accountant.employee == request.user:
            return True

        return False