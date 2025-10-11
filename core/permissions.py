from rest_framework.permissions import BasePermission

class AdminPermission(BasePermission):
    required_roles = ["Admin"]

    def has_permission(self, request, view):
        if not request.user or request.user.is_anonymous:
            return False
        
        # Check for roles in the decoded token dictionary
        user_roles = request.user.get("roles", [])
        if any(role in self.required_roles for role in user_roles):
            return True
        return False
    
class FinancePermission(BasePermission):
    required_roles = ["Finance"]

    def has_permission(self, request, view):
        if not request.user or request.user.is_anonymous:
            return False
        
        # Check for roles in the decoded token dictionary
        user_roles = request.user.get("roles", [])
        print(user_roles)
        if any(role in self.required_roles for role in user_roles):
            return True
        return False
    
class UserPermission(BasePermission):
    required_roles = ["User"]

    def has_permission(self, request, view):
        if not request.user or request.user.is_anonymous:
            return False
        
        # Check for roles in the decoded token dictionary
        user_roles = request.user.get("roles", [])
        if any(role in self.required_roles for role in user_roles):
            return True
        return False