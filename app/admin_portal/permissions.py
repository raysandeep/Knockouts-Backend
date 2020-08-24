from rest_framework.permissions import BasePermission


class IsDSCModerator(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool(request.user and request.user.is_admin)
        else:
            return False


class IsDSCQuestionModerator(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool(request.user and request.user.is_admin and request.user.is_staff)
        else:
            return False
