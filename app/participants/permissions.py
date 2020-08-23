from rest_framework.permissions import BasePermission
from admin_portal.models import Rounds
from django.utils import timezone


class IsnotDisqualified(BasePermission):
    def has_permission(self, request, view):
        request_datetime = timezone.now()
        round = Rounds.objects.filter(start_time__lte=request_datetime,
                                      end_time__gte=request_datetime)
        print(round.exists())
        if not round.exists():
            return False
        return bool(request.user and not request.user.is_disqualified and not request.user.is_blocked)

class IsObjOwner(BasePermission):
    message = "You don't have access to update this "

    def has_object_permission(self, request, view, obj):
        return bool(request.user and not request.user.is_disqualified and not request.user.is_blocked and obj.room_seat.participant == request.user)