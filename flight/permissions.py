from rest_framework.permissions import BasePermission, IsAdminUser

class IsAdminUserOrReadOnly(BasePermission):
    
    SAFE_METHODS = ['GET', 'OPTIONS', 'HEAD']
    def has_permission(self, request, view):
        if request.method in self.SAFE_METHODS:
            return True
        return IsAdminUser().has_permission(request, view)