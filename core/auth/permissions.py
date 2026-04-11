from rest_framework.permissions import BasePermission
from core.models import AppUser

def get_roles(user_id):
    roles_data = AppUser.objects.filter(oid=user_id).values("roles").first()

    # Get the inner list from the data
    roles = roles_data["roles"] if roles_data else []

    return roles

def get_permissions(user_id):
    permissions_data = AppUser.objects.filter(oid=user_id).values("permissions").first()

    # Get the inner list from the data
    permissions = permissions_data["permissions"] if permissions_data else []

    return permissions

class IsAuthenticated(BasePermission):
    """
    Check if a user has been authenticated. Anonymous users are not allowed.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated or request.user.is_anonymous:
            return False

        return True

class AdminRole(BasePermission):
    required_roles = ["Admin"]

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated or request.user.is_anonymous:
            return False

        roles = get_roles(request.user.oid)

        if any(role in self.required_roles for role in roles):
            return True

        return False

class UserRole(BasePermission):
    required_roles = ["User"]

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated or request.user.is_anonymous:
            return False

        roles = get_roles(request.user.oid)

        if any(role in self.required_roles for role in roles):
            return True

        return False

class ITRole(BasePermission):
    required_roles = ["IT"]

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated or request.user.is_anonymous:
            return False

        roles = get_roles(request.user.oid)

        print (roles)

        if any(role in self.required_roles for role in roles):
            return True

        return False

class HrRole(BasePermission):
    required_roles = ["HR"]

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated or request.user.is_anonymous:
            return False

        roles = get_roles(request.user.oid)

        if any(role in self.required_roles for role in roles):
            return True

        return False