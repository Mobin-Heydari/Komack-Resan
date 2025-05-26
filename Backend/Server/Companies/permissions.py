from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Company

class IsAdminOrOwner(BasePermission):
    """
    Custom permission that allows write access only to admin users or users whose 
    `user_type` equals 'OW' (Owner). Read access is granted to everyone.
    """
    def has_permission(self, request, view):
        # Allow safe methods without additional checks.
        if request.method in SAFE_METHODS:
            return True

        # Verify that the user is authenticated and either is staff or of user_type 'OW'
        return (
            request.user and request.user.is_authenticated and
            (request.user.is_staff or getattr(request.user, 'user_type', '').upper() == 'OW')
        )

    def has_object_permission(self, request, view, obj):
        # Allow safe methods without object-level checks.
        if request.method in SAFE_METHODS:
            return True

        # For unsafe methods, allow access if the user is an admin or is the employer (owner) of the company.
        return request.user.is_staff or obj.employer == request.user


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission that allows only admin users to create, update, or delete items.
    Read operations (GET, HEAD, OPTIONS) are permitted for all users.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True  # Allow read actions for everyone
        return request.user and request.user.is_authenticated and request.user.is_staff


# Permission for list action: only admin (is_staff) can list.
class IsAdminOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff
    

# Permission for retrieve and update: only admin or the company's employer may access.
class IsAdminOrEmployer(BasePermission):
    def has_object_permission(self, request, view, obj):
        # obj is a CompanyValidationStatus instance; check that its related company.employer
        return request.user and (request.user.is_staff or obj.company.employer == request.user)
    


class IsAdminOrCompanyEmployer(BasePermission):
    """
    Custom permission to allow only admins or the employer (owner) of the company to modify
    CompanyFirstItem/CompanySecondItem resources.
    
    - For safe methods (GET, HEAD, OPTIONS): allow access.
    - For write actions (POST, PUT, PATCH, DELETE):
         • If no object is available (e.g. on create), the permission checks that the request data
           contains a valid 'company_slug' identifying a Company and that the requesting user is either
           an admin or is the employer of that Company.
         • For object-level operations (update/delete), it checks that the user is either admin or matches
           the company.employer on the instance (where the FK is stored in the `compay` field).
    """
    def has_permission(self, request, view):
        # Allow safe methods for all users.
        if request.method in SAFE_METHODS:
            return True

        # Must be authenticated for write operations.
        if not request.user or not request.user.is_authenticated:
            return False

        # For creation (i.e. no object yet), verify that request.data contains a valid company_slug.
        if request.method == 'POST':
            company_slug = request.data.get('company_slug')
            if not company_slug:
                return False  # company_slug is required on create.
            try:
                company = Company.objects.get(slug=company_slug)
            except Company.DoesNotExist:
                return False
            return request.user.is_staff or (company.employer == request.user)
        
        # For other methods (PUT, PATCH, DELETE) that have an associated object, defer to has_object_permission.
        return True

    def has_object_permission(self, request, view, obj):
        # Allow safe methods.
        if request.method in SAFE_METHODS:
            return True
        
        # For unsafe methods, allow if the user is admin or if the employer of the item's company matches.
        return request.user.is_staff or (obj.compay.employer == request.user)



class IsCompanyEmployeeOwnerOrAdmin(BasePermission):
    """
    Custom permission for managing company employee records.
    
    For list:
      - Anyone who is authenticated can list, but the viewset will filter the queryset
        (admin: all records; non-admin owner: only records belonging to their company).
      
    For create (POST):
      - If the user is admin, allow.
      - Otherwise, examine request.data for a 'company_slug' and only allow if the company’s employer matches the user.

    For object-level actions (retrieve, update, destroy):
      - Allow admins.
      - For safe methods (GET), allow if the request user is the record’s employee or the company's employer.
      - For update and delete, allow only if the request user is the company’s employer.
    """
    
    def has_permission(self, request, view):
        # Allow safe methods; object-level checks will work later.
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        # For creation, check for 'company_slug' in the request data.
        if request.method == "POST":
            if request.user.is_staff:
                return True
            company_slug = request.data.get('company_slug')
            if not company_slug:
                return False
            # Lazy import to avoid circular dependency
            from Companies.models import Company  
            try:
                company = Company.objects.get(slug=company_slug)
            except Company.DoesNotExist:
                return False
            return company.employer == request.user

        # For PUT/PATCH/DELETE, we return True here and let object-level permission handle the details.
        return True

    def has_object_permission(self, request, view, obj):
        # Admin users have full access.
        if request.user.is_staff:
            return True
        
        # For safe methods (GET, HEAD, OPTIONS), allow if the current user is either the employee or the company employer.
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return request.user == obj.employee or request.user == obj.company.employer
        
        # For non-safe methods (PUT, PATCH, DELETE),
        # only allow if the current user is the company employer.
        return request.user == obj.company.employer
