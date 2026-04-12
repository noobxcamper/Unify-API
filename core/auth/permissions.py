from rest_framework.permissions import BasePermission
from core.models import AppUsers

def get_user_access(user_id):
    data = (AppUsers.objects.filter(oid=user_id).values("roles", "permissions").first()) or {}

    return {
        "roles": data.get("roles", []) or [],
        "permissions": data.get("permissions", []) or [],
    }


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and not user.is_anonymous)


class BaseAccessPermission(BasePermission):
    required_roles = []
    required_permissions = []

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated or user.is_anonymous:
            return False

        access = get_user_access(user.oid)

        return (
            any(r in self.required_roles for r in access["roles"]) or
            any(p in self.required_permissions for p in access["permissions"])
        )


class AdminRole(BaseAccessPermission):
    required_roles = ["Admin"]


class UserRole(BaseAccessPermission):
    required_roles = ["User"]


class ITRole(BaseAccessPermission):
    required_roles = ["IT"]


class HrRole(BaseAccessPermission):
    required_roles = ["HR"]


class AutomationAdminRole(BaseAccessPermission):
    required_roles = ["AutomationAdministrator"]