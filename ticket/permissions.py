from rest_framework.permissions import BasePermission, IsAdminUser

class TicketPermission(BasePermission):

    SAFE_METHODS = ['POST', 'OPTIONS', 'HEAD', 'GET', 'DELETE']
    def has_permission(self, request, view):
        if request.method in self.SAFE_METHODS:
            return True
        return IsAdminUser().has_permission(request, view)
        
        