from rest_framework.permissions import BasePermission

class IsnotDisqualified(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and not request.user.is_disqualified and not request.user.is_blocked)

class IsObjOwner(BasePermission):
    message = "You don't have access to update this "

    def has_object_permission(self, request, view, obj):
        return bool(request.user and not request.user.is_disqualified and not request.user.is_blocked and obj.owner == request.user)