from rest_framework.permissions import BasePermission

class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'moderator'

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class IsSeller(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'seller'

class IsBuyer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'buyer'

class IsAdminOrModerator(BasePermission):
    def has_permission(self, request, view):
        return (IsAdmin().has_permission(request, view) or
            IsModerator().has_permission(request, view))

class IsSellerOrAdminOrModerator(BasePermission):
    def has_permission(self, request, view):
        return (
            IsSeller().has_permission(request, view) or
            IsAdminOrModerator().has_permission(request, view)
        )


