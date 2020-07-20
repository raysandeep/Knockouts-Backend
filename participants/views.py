from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView,RetrieveAPIView,ListAPIView,UpdateAPIView
from .permissions import (
    IsnotDisqualified
)
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from admin_portal.models import (
    Rounds,
    RoomParticipantAbstract,
    Rooms,
    RoomParticipantManager
)
from .serializers import(
    RoomParticipantAbstractSerializer,
    RoomParticipantSerializer,
    RoomParticipantUpdateSerializer
)

class DashBoardListAPIView(ListAPIView):
    serializer_class = RoomParticipantAbstractSerializer
    permission_classes = [IsnotDisqualified]
    parsers = [JSONParser]
    
    def get_queryset(self,request):
        request_datetime = request.META.get('HTTP_DATE')
        round = Rounds.objects.filter(start_time__lte=request_datetime,
                     end_time__gte=request_datetime)
        if not round.exists():
            return []
        user_dash = RoomParticipantAbstract.objects.prefetch_related('room').filter(
            participant=request.user
                ).filter(room__round=round[0])
        return user_dash

class CodeRetrieveAPIView(RetrieveAPIView):
    queryset = RoomParticipantManager.objects.all()
    serializer_class = RoomParticipantSerializer
    permission_classes = [IsnotDisqualified]
    parsers = [JSONParser]
    def get_queryset(self,request):
        return RoomParticipantManager.objects.filter(room_seat__participant=request.user)

class CodeUpdateAPIView(UpdateAPIView):
    queryset = RoomParticipantManager.objects.all()
    serializer_class = RoomParticipantUpdateSerializer
    permission_classes = [IsnotDisqualified]
    parsers = [JSONParser]
    def get_queryset(self,request):
        id = ''
        if request.data['id']:
            id = request.data['id']
    
        return RoomParticipantManager.objects.filter(room_seat__participant=request.user).filter(room_seat__id=id)


# class CodeRun(APIView):
