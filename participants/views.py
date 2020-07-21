from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView,RetrieveAPIView,ListAPIView,RetrieveUpdateAPIView
from .permissions import (
    IsnotDisqualified,
    IsObjOwner
)
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from admin_portal.models import (
    Rounds,
    RoomParticipantAbstract,
    Rooms,
    RoomParticipantManager,
    TestCaseSolutionLogger,
    TestCaseHolder,
    QuestionsModel
)
from .serializers import(
    RoomParticipantAbstractSerializer,
    RoomParticipantSerializer,
    RoomParticipantUpdateSerializer,
    QuestionSerializer,
    QuestionAdminSerializer
)
from django.utils import timezone
import pytz
from rest_framework.permissions import IsAdminUser


class DashBoardListAPIView(ListAPIView):
    serializer_class = RoomParticipantAbstractSerializer
    permission_classes = [IsnotDisqualified]
    parsers = [JSONParser]
    
    def get_queryset(self):
        request_datetime = timezone.now()
        print(request_datetime)
        round = Rounds.objects.filter(start_time__lte=request_datetime,
                     end_time__gte=request_datetime)
        print(round)
        print(round.count())
        if not round.exists():
            return []
        user_dash = RoomParticipantAbstract.objects.prefetch_related('room').filter(
            participant=self.request.user
                ).filter(room__round__in=round)
        print(user_dash)
        print(user_dash.count())
        return user_dash

class CodeRetrieveAPIView(RetrieveUpdateAPIView):
    queryset = RoomParticipantManager.objects.all()
    permission_classes = [IsObjOwner]
    parsers = [JSONParser]
    
    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return RoomParticipantUpdateSerializer
        return RoomParticipantSerializer

class CodeCreateAPIView(CreateAPIView):
    queryset = RoomParticipantManager.objects.all()
    serializer_class = RoomParticipantUpdateSerializer
    permission_classes = [IsnotDisqualified]
    def get_queryset(self):
        id = ''
        if self.request.data['id']:
            id = self.request.data['id']
        return RoomParticipantManager.objects.filter(room_seat__participant=self.request.user).filter(room_seat__id=id)


class QuestionAndTestCaseGETAPIView(RetrieveAPIView):
    queryset = QuestionsModel.objects.filter()
    serializer_class = QuestionSerializer
    permission_classes = [IsObjOwner]
    parsers = [JSONParser]

class CodeRetrieveAPIView(RetrieveAPIView):
    queryset = RoomParticipantManager.objects.all()
    permission_classes = [IsAdminUser]
    parsers = [JSONParser]
    serializer_class = RoomParticipantSerializer


class TestCaseAPIView(RetrieveAPIView):
    queryset = QuestionsModel.objects.all()
    permission_classes = [IsAdminUser]
    parsers = [JSONParser]
    serializer_class = QuestionAdminSerializer