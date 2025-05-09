from rest_framework.permissions import BasePermission, SAFE_METHODS


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