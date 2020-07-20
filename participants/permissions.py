from rest_framework.permissions import BasePermission


class IsnotDisqualified(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and not request.user.is_disqualified and not request.user.is_blocked)