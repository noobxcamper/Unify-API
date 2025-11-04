from rest_framework.permissions import BasePermission

class IsSuperuserStrict(BasePermission):
    """
    Check if the user is a superuser in the django admin panel. User must be a superuser and member of staff.

    Anonymous users are not allowed.
    """
    def has_permission(self, request, view):
        if not request.user or request.user.is_anonymous:
            return False

        if request.user.is_superuser and request.user.is_staff:
            return True

        return False

class AdminPermission(BasePermission):
    """
    Extends the django rest framework permission class to control endpoint access
    based on the roles provided in the access token.
    """
    required_roles = ["Admin"]

    def has_permission(self, request, view):
        if not request.user or request.user.is_anonymous:
            return False
        
        # Check for roles in the decoded token dictionary
        user_roles = request.user.get("roles", [])
        if any(role in self.required_roles for role in user_roles):
            return True
        return False
    
class UserPermission(BasePermission):
    """
    Extends the django rest framework permission class to control endpoint access
    based on the roles provided in the access token.
    """

    required_roles = ["User"]

    def has_permission(self, request, view):
        if not request.user or request.user.is_anonymous:
            return False
        
        # Check for roles in the decoded token dictionary
        user_roles = request.user.get("roles", [])
        if any(role in self.required_roles for role in user_roles):
            return True
        return False