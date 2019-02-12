from rest_framework.permissions import BasePermission, IsAdminUser, IsAuthenticated

class TicketPermission(BasePermission):

    SAFE_METHODS = ['POST', 'OPTIONS', 'HEAD', 'GET']
    def has_permission(self, request, view):
        if IsAuthenticated().has_permission(request, view) and request.method in self.SAFE_METHODS:
            return True
        return IsAdminUser().has_permission(request, view)