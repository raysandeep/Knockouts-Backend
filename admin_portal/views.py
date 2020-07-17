from django.shortcuts import render
from rest_framework.generics import CreateAPIView,RetrieveUpdateDestroyAPIView,ListAPIView
from .permissions import IsDSCModerator,IsDSCQuestionModerator
from .models import (
    QuestionsModel,
    TestCaseHolder,
    Rounds
)
from .serializers import(
    QuestionSerializer,
    TestCaseSerializer,
    AdminQuestionSerializer,
    RoundSerializer,
)
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import User
import math
from admin_portal.models import RoomParticipantAbstract, Rooms
from rest_framework.permissions import IsAdminUser


class QuestionCreateAPIView(CreateAPIView):
    queryset = QuestionsModel.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsDSCModerator]
    parsers = [JSONParser]


class QuestionUpdateAPIView(RetrieveUpdateDestroyAPIView):
    queryset = QuestionsModel.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsDSCQuestionModerator]
    parsers = [JSONParser]

    def get_serializer_class(self):
        if self.request.user.is_admin and self.request.user.is_staff:
            return AdminQuestionSerializer
        return QuestionSerializer


class QuestionsListAPIView(ListAPIView):
    queryset = QuestionsModel.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsDSCModerator]
    parsers = [JSONParser]


class TestCaseCreateAPIView(CreateAPIView):
    queryset = TestCaseHolder.objects.all()
    serializer_class = TestCaseSerializer
    permission_classes = [IsDSCModerator]
    parsers = [JSONParser]

class TestCasesListAPIView(ListAPIView):
    lookup_url_kwarg = "question"
    serializer_class = TestCaseSerializer
    permission_classes = [IsDSCModerator]
    parsers = [JSONParser]
    
    def get_queryset(self):
        question_id = self.kwargs.get(self.lookup_url_kwarg)
        testcase_list = TestCaseHolder.objects.filter(question=question_id)
        return testcase_list

class TestCaseUpdateAPIView(RetrieveUpdateDestroyAPIView):
    queryset = TestCaseHolder.objects.all()
    serializer_class = TestCaseSerializer
    permission_classes = [IsDSCQuestionModerator]
    parsers = [JSONParser]

class RoundCreateAPIView(CreateAPIView):
    queryset = Rounds.objects.all()
    serializer_class = RoundSerializer
    permission_classes = [IsDSCQuestionModerator]
    parsers = [JSONParser]


class RoundUpdateAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Rounds.objects.all()
    serializer_class = RoundSerializer
    permission_classes = [IsDSCQuestionModerator]
    parsers = [JSONParser]


class RoundListAPIView(ListAPIView):
    queryset = Rounds.objects.all()
    serializer_class = RoundSerializer
    permission_classes = [IsDSCQuestionModerator]
    parsers = [JSONParser]


class AssignPeopleAPIView(APIView):
    permission_classes = [IsAdminUser]
    def get_round_queryset(self,id):
        print(id)
        round_query = Rounds.objects.filter(id=id)
        print(round_query.exists())
        if round_query.exists():
            return  True,round_query
        return False,[]

    # very heavy route. 
    def post(self,request):
        if not request.data['round']:
            return Response({'status':'Round is a compulsary field!'},status=400)
        status, queryset = self.get_round_queryset(request.data['round'])
        print(status, queryset)
        if not status:
            return Response({'status':'Round doesn\'t exist'},status=400)

        #get questions 

        questions = QuestionsModel.objects.filter(
                    is_verified=True
                ).filter(
                    is_assigned=False).filter(
                        difficulty_level__range=(
                            0, queryset[0].difficulty_allowance
                            )).order_by('?')

        #error debugging 
        for i in questions:
            print(i.id)


        questions_count = questions.count()
        users = User.objects.filter(is_admin=False).filter(is_disqualified=False).order_by('?')
        teams_count = math.floor(users.count()/2)
        if teams_count>questions_count:
            return Response({
                'status':'failed',
                'message':'Questions not sufficient.',
                'questions_count':questions_count,
                'teams_count':teams_count
                },status=206)

        room_participants = []
        room_list = []
        print("questions : "+str(questions_count))
        print("teams     : "+str(teams_count))

        #Make Teams and Assign questions 
        for i in range(teams_count):
            room_dicti = {
                'question' : questions[i],
                'round':queryset[0]
            }
            print(room_dicti)
            room = Rooms(**room_dicti)
            participant1 = {
                'room':room,
                'participant':users[i]
            }
            participant2 = {
                'room':room,
                'participant':users[teams_count+i]
            }
            parti1room = RoomParticipantAbstract(**participant1)
            parti2room = RoomParticipantAbstract(**participant2)

            room_list.append(room)
            room_participants.append(parti1room)
            room_participants.append(parti2room)
        print('\n\n\n')
        print(room_list)
        print('\n\n\n')
        print(room_participants)
        Rooms.objects.bulk_create(room_list)
        RoomParticipantAbstract.objects.bulk_create(room_participants)
        return Response({
            'status':'success'
        },status=200)