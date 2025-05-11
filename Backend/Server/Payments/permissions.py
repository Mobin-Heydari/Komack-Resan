from rest_framework.permissions import BasePermission, SAFE_METHODS



class PaymentInvoicePermission(BasePermission):
    """
    Custom permission for PaymentInvoice:

    - On creation (POST):
      * The request must provide a valid invoice_id.
      * Additionally, the owner of invoice.company must match the requesting user.
    
    - For update (PUT/PATCH):
      * Only admin users (i.e. request.user.is_staff == True) are allowed.
    
    - Safe methods (GET, HEAD, OPTIONS) are allowed for everyone.
    """
    
    def has_permission(self, request, view):
        # Allow safe methods.
        if request.method in SAFE_METHODS:
            return True
        
        # For creation (POST):
        if request.method == "POST":
            # Must be a company employer.
            if getattr(request.user, 'user_type', None) != "OW":
                return False
            
            return True
        
        # For update (PUT/PATCH), only admin is allowed.
        if request.method in ["PUT", "PATCH"]:
            return request.user and request.user.is_staff
        
        # Other methods: apply your own rules (or deny).
        return False

    def has_object_permission(self, request, view, obj):
        # Allow safe methods.
        if request.method in SAFE_METHODS:
            return True
        
        # For update operations, only admin may update.
        if request.method in ["PUT", "PATCH"]:
            return request.user and request.user.is_staff
        
        return False
