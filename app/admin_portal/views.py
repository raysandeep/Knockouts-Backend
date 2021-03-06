from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView, \
    DestroyAPIView
from .permissions import IsDSCModerator, IsDSCQuestionModerator
from .models import (
    QuestionsModel,
    TestCaseHolder,
    Rounds,
    RoomParticipantManager,
    DisQualifyModel
)
from .serializers import (
    QuestionSerializer,
    TestCaseSerializer,
    AdminQuestionSerializer,
    RoundSerializer,
    RoomsSerializer,
    RoomParticipantAbstractSerializer,
    DisQualifySerailizer
)
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import User
import math
from admin_portal.models import RoomParticipantAbstract, Rooms
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from accounts.serializers import (
    UserSignupSerializer
)


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
    queryset = QuestionsModel.objects.filter(id="3ab2886f-f852-448f-a19a-65e91884ce43")
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

    def get_round_queryset(self, id):
        print(id)
        round_query = Rounds.objects.filter(id=id)
        print(round_query.exists())
        if round_query.exists():
            return True, round_query
        return False, []

    # very heavy route. 
    def post(self, request):
        if not request.data['round']:
            return Response({'status': 'Round is a compulsary field!'}, status=400)
        status, queryset = self.get_round_queryset(request.data['round'])
        print(status, queryset)
        if not status:
            return Response({'status': 'Round doesn\'t exist'}, status=400)

        # get questions

        questions = QuestionsModel.objects.filter(
            is_verified=True
        ).filter(
            is_assigned=False).filter(
            difficulty_level=queryset[0].difficulty_allowance
        ).order_by('difficulty_level')

        questions_count = questions.count()
        users = User.objects.filter(is_admin=False).filter(is_disqualified=False)
        teams_count = math.floor(users.count() / 2)
        if teams_count > questions_count:
            return Response({
                'status': 'failed',
                'message': 'Questions not sufficient.',
                'questions_count': questions_count,
                'teams_count': teams_count
            }, status=206)

        room_participants = []
        room_list = []
        print("questions : " + str(questions_count))
        print("teams     : " + str(teams_count))

        # Make Teams and Assign questions
        for i in range(teams_count):
            room_dicti = {
                'question': questions[i],
                'round': queryset[0]
            }
            print(room_dicti)
            room = Rooms(**room_dicti)
            participant1 = {
                'room': room,
                'participant': users[i]
            }
            participant2 = {
                'room': room,
                'participant': users[teams_count + i]
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
        inner_q = questions[0:teams_count]
        QuestionsModel.objects.filter(id__in=inner_q).update(is_assigned=1)
        return Response({
            'status': 'success'
        }, status=200)


class GetAllRoomsListAPIView(ListAPIView):
    lookup_url_kwarg = "round"
    serializer_class = RoomParticipantAbstractSerializer
    permission_classes = [IsDSCQuestionModerator]
    parsers = [JSONParser]

    def get_queryset(self):
        round_id = self.kwargs.get(self.lookup_url_kwarg)
        print(round_id)
        room_query = RoomParticipantAbstract.objects.filter(room__round=round_id)
        print(room_query.count())
        return room_query


class GetPendingPplAPIView(ListAPIView):
    lookup_url_kwarg = "round"
    serializer_class = UserSignupSerializer
    permission_classes = [IsDSCModerator]
    parsers = [JSONParser]

    def get_queryset(self):
        round_id = self.kwargs.get(self.lookup_url_kwarg)
        users_ids = RoomParticipantAbstract.objects.prefetch_related(
            'participant'
        ).filter(
            room__round=round_id
        ).values_list('participant__id', flat=True)
        room = User.objects.filter(is_admin=False).filter(is_disqualified=False).exclude(id__in=users_ids)
        return room


class RoomCreateAPIView(APIView):
    permission_classes = [IsDSCModerator]
    parsers = [JSONParser]

    def get_round_queryset(self, id):
        print(id)
        round_query = Rounds.objects.filter(id=id)
        print(round_query.exists())
        if round_query.exists():
            return True, round_query[0]
        return False, []

    def post(self, request):
        username1 = request.data['username1']
        username2 = request.data['username2']
        round = request.data['round']

        queryset1 = User.objects.filter(username=username1)
        if not queryset1.exists():
            return Response({'data': 'No account found'}, status=400)

        queryset2 = User.objects.filter(username=username2)
        if not queryset1.exists():
            return Response({'data': 'No account found'}, status=400)

        status, queryset = self.get_round_queryset(round)
        print(status, queryset)
        if not status:
            return Response({'data': 'No round found'}, status=400)

        questions = QuestionsModel.objects.filter(
            is_verified=True
        ).filter(
            is_assigned=False).filter(
            difficulty_level=queryset.difficulty_allowance
        ).order_by('difficulty_level')
        questions_count = questions.count()

        if questions_count == 0:
            return Response({'data': 'No questions found!'}, status=400)

        dicti = {
            "question": questions[0],
            'round': queryset
        }
        room = Rooms(**dicti)

        dicti1 = {
            'room': room,
            'participant': queryset1[0]
        }

        dicti2 = {
            'room': room,
            'participant': queryset2[0]
        }
        room_abs1 = RoomParticipantAbstract(**dicti1)
        room_abs2 = RoomParticipantAbstract(**dicti2)
        questions[0].is_assigned = True
        room.save()
        questions[0].save()
        room_abs1.save()
        room_abs2.save()
        return Response(status=204)


class RoomRetrieveAPIView(RetrieveAPIView):
    queryset = Rooms.objects.all()
    serializer_class = RoomsSerializer
    permission_classes = [IsDSCModerator]
    parsers = [JSONParser]


class RoomDestroyAPIView(DestroyAPIView):
    queryset = Rooms.objects.all()
    serializer_class = RoomsSerializer
    permission_classes = [IsDSCModerator]
    parsers = [JSONParser]


class DisQualifyUsers(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id):
        query = Rooms.objects.filter(round=id)
        disqualifed_users = []
        if query.count() == 0:
            return Response(status=404)
        for i in query:
            partiticipants = RoomParticipantAbstract.objects.filter(room=i.id)
            for j in partiticipants:
                try:
                    user_manager = j.roomparticipantmanager
                except Exception as e:
                    print(e)
                    dicti = {
                        "room_seat": j,
                        "current_code": "print('Default Submission')",
                        "language_of_code": 71

                    }
                    manager = RoomParticipantManager(**dicti)
                    manager.save()
                    disqualifed_users.append(j.participant.username)
        return Response(disqualifed_users, status=201)

    def post(self, request, id):
        query = Rooms.objects.filter(round=id)
        disqualifed_users = []
        if query.count() == 0:
            return Response(status=404)
        for i in query:
            partiticipants = RoomParticipantAbstract.objects.filter(room=i.id)
            for j in partiticipants:
                try:
                    user_manager = j.roomparticipantmanager
                except Exception as e:
                    print(e)
                    dicti = {
                        "room_seat": j,
                        "current_code": "print('Default Submission')",
                        "language_of_code": 71

                    }
                    manager = RoomParticipantManager(**dicti)
                    manager.save()
                    disqualifed_users.append(j.participant.username)
        for i in query:
            partiticipants = RoomParticipantManager.objects.filter(room_seat__room=i.id).order_by('-score')
            for j in range(1, len(partiticipants)):
                disqualify = partiticipants[j].room_seat.participant
                disqualify.is_disqualified = True
                disqualify.save()
                disqualifed_users.append(disqualify.username)
        users = {
            'count': len(disqualifed_users),
            'users': disqualifed_users
        }
        final_dicti = {
            'dis_round': Rounds.objects.filter(id=id)[0],
            'users': users
        }
        store_status = DisQualifyModel(**final_dicti)
        store_status.save()
        return Response(users, status=201)


class DisQualifiedUsersGet(APIView):
    permission_classes = [IsDSCModerator]

    def get(self, request, id):
        query = DisQualifyModel.objects.filter(dis_round__id=id)
        serializer = DisQualifySerailizer(query, many=True)
        return Response(serializer.data, status=201)
