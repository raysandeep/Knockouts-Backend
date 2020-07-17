from rest_framework.permissions import BasePermission


class IsDSCModerator(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_admin)

class IsDSCQuestionModerator(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_admin and request.user.is_staff)
