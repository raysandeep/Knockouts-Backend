import requests
from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, RetrieveUpdateAPIView
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
from .serializers import (
    RoomParticipantAbstractSerializer,
    RoomParticipantSerializer,
    RoomParticipantUpdateSerializer,
    QuestionSerializer,
    QuestionAdminSerializer, TestCasesSolutionSerailizer
)
from django.utils import timezone
import pytz
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny
from django.conf import settings
import math
from django.core.cache import cache
from accounts.models import User
import requests as rq
import base64
from django.db.models import Sum

SAMPLE_JSON = {
    "data": [{
        "id": 46,
        "time": 0.5,
        "name": "Bash (5.0.0)"
    },
        {
            "id": 75,
            "time": 1,
            "name": "C (Clang 7.0.1)"
        },
        {
            "id": 76,
            "time": 1,
            "name": "C++ (Clang 7.0.1)"
        },
        {
            "id": 48,
            "time": 1,
            "name": "C (GCC 7.4.0)"
        },
        {
            "id": 52,
            "time": 1,
            "name": "C++ (GCC 7.4.0)"
        },
        {
            "id": 49,
            "time": 1,
            "name": "C (GCC 8.3.0)"
        },
        {
            "id": 53,
            "time": 1,
            "name": "C++ (GCC 8.3.0)"
        },
        {
            "id": 50,
            "time": 1,
            "name": "C (GCC 9.2.0)"
        },
        {
            "id": 54,
            "time": 1,
            "name": "C++ (GCC 9.2.0)"
        },
        {
            "id": 86,
            "time": 4,
            "name": "Clojure (1.10.1)"
        },
        {
            "id": 51,
            "time": 2,
            "name": "C# (Mono 6.6.0.161)"
        },
        {
            "id": 56,
            "time": 1.5,
            "name": "D (DMD 2.089.1)"
        },
        {
            "id": 58,
            "time": 6,
            "name": "Erlang (OTP 22.2)"
        },
        {
            "id": 87,
            "time": 2,
            "name": "F# (.NET Core SDK 3.1.202)"
        },
        {
            "id": 59,
            "time": 1,
            "name": "Fortran (GFortran 9.2.0)"
        },
        {
            "id": 60,
            "time": 2,
            "name": "Go (1.13.5)"
        },
        {
            "id": 88,
            "time": 2.5,
            "name": "Groovy (3.0.3)"
        },
        {
            "id": 61,
            "time": 3,
            "name": "Haskell (GHC 8.8.1)"
        },
        {
            "id": 62,
            "time": 2,
            "name": "Java (OpenJDK 13.0.1)"
        },
        {
            "id": 63,
            "time": 5,
            "name": "JavaScript (Node.js 12.14.0)"
        },
        {
            "id": 78,
            "time": 2,
            "name": "Kotlin (1.3.70)"
        },
        {
            "id": 64,
            "time": 6,
            "name": "Lua (5.3.5)"
        },
        {
            "id": 79,
            "time": 1,
            "name": "Objective-C (Clang 7.0.1)"
        },
        {
            "id": 65,
            "time": 1.5,
            "name": "OCaml (4.09.0)"
        },
        {
            "id": 67,
            "time": 1,
            "name": "Pascal (FPC 3.0.4)"
        },
        {
            "id": 85,
            "time": 5,
            "name": "Perl (5.28.1)"
        },
        {
            "id": 68,
            "time": 5,
            "name": "PHP (7.4.1)"
        },
        {
            "id": 70,
            "time": 5,
            "name": "Python (2.7.17)"
        },
        {
            "id": 71,
            "time": 5,
            "name": "Python (3.8.1)"
        },
        {
            "id": 80,
            "time": 1.5,
            "name": "R (4.0.0)"
        },
        {
            "id": 72,
            "time": 5,
            "name": "Ruby (2.7.0)"
        },
        {
            "id": 73,
            "time": 2.5,
            "name": "Rust (1.40.0)"
        },
        {
            "id": 81,
            "time": 3.5,
            "name": "Scala (2.13.2)"
        },
        {
            "id": 83,
            "time": 1,
            "name": "Swift (5.2.3)"
        },
        {
            "id": 74,
            "time": 5,
            "name": "TypeScript (3.7.4)"
        },
        {
            "id": 84,
            "time": 2.5,
            "name": "Visual Basic.Net (vbnc 0.0.0.5943)"
        }
    ]
}


def getTimeLimit(id):
    for i in SAMPLE_JSON["data"]:
        if i["id"] == id:
            return i["time"]

    return 2.5


def sendRequest(data, room_id, count):
    headers = {
        'Content-Type': 'application/json'
    }
    response = rq.request("POST", settings.JUDGEAPI_URL, headers=headers, json=data)
    tokens = []
    print(response.status_code)
    print(data)
    if response.status_code == 201:
        for i in response.json():
            tokens.append(i["token"])
        if cache.set(room_id + "__count", count, timeout=60 * 5):
            return True, tokens
    return False, []


def sendTriggertofastapi(room_name):
    headers = {
        'Content-Type': 'application/json'
    }
    response = rq.request("GET", settings.FASTAPI_URL + 'trigger/' + room_name)
    if response.status_code == 200:
        return True
    return False


def sendRedis(room_name, token, status):
    count = int(cache.get(room_name + "__count")) - 1

    ttl = cache.ttl(room_name + "__count")
    cache.set(room_name + "__count", str(count), timeout=ttl)

    if count == 0:
        sendTriggertofastapi(room_name)

    return True


class DashBoardListAPIView(ListAPIView):
    serializer_class = RoomParticipantAbstractSerializer
    permission_classes = [IsnotDisqualified]
    parsers = [JSONParser]

    def get_queryset(self):
        request_datetime = timezone.now()
        round = Rounds.objects.filter(start_time__lte=request_datetime,
                                      end_time__gte=request_datetime)
        if not round.exists():
            return []
        user_dash = RoomParticipantAbstract.objects.prefetch_related('room').filter(
            participant=self.request.user
        ).filter(room__round__in=round)
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
    permission_classes = [IsAuthenticatedOrReadOnly]
    parsers = [JSONParser]


def dobase64encode(tobeencoded):
    if tobeencoded is None:
        return 'null'
    else:
        return base64.b64encode(tobeencoded.encode("ascii")).decode("ascii")


def dobase64decode(tobedecoded):
    if tobedecoded is None:
        return "NULL"
    else:
        return base64.b64decode(tobedecoded.encode("ascii")).decode("ascii")


class CallBackHandler(APIView):
    parsers = [JSONParser]
    permission_classes = [AllowAny]

    def put(self, request, roomabsid, testid):
        data = request.data
        room = RoomParticipantManager.objects.filter(id=roomabsid)
        test_case = TestCaseHolder.objects.filter(id=testid)
        status = False
        if data['status']['id'] == 3:
            status = True
        output = dobase64decode(data['stdout'])
        print(output)
        print(data['status']['id'])
        dicti = {
            'room_solution': room[0],
            'test_case': test_case[0],
            'stdin': test_case[0].stdin,
            'stdout': output,
            'time': data['time'],
            'memory': data['memory'],
            'error': dobase64decode(data['stderr']),
            'token': data['status']['id'],
            'is_solved': status,
            "score_for_this_testcase": settings.MARKS_FOR_EACH_QUES
        }

        print(dicti)
        testcase = TestCaseSolutionLogger(**dicti)
        testcase.save()

        sendRedis(roomabsid, data['token'], status)
        return Response(status=200)


class SubmitQuestion(APIView):
    permission_classes = [IsnotDisqualified]
    parsers = [JSONParser]

    def post(self, request):
        data = {
            'secret': settings.GOOGLE_RECAPTCHA,
            'response': request.data.get('g_token', None)
        }

        resp = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data=data
        )

        print(resp.json())

        if not resp.json().get('success'):
            return Response(data={'message': 'ReCAPTCHA not verified!'}, status=406)

        try:
            id = request.data["id"]
            question_id = request.data["question_id"]
        except:
            return Response(status=400)
        # get room

        room = RoomParticipantManager.objects.filter(id=id)
        if not room.exists():
            return Response(status=400)
        elif room.exists() and room[0].is_submitted:
            return Response({"message": "Already Submitted"}, status=208)

        else:
            # get code
            testcases = TestCaseSolutionLogger.objects.filter(room_solution=id)
            testcases.delete()
            language_id = room[0].language_of_code
            current_code = room[0].current_code
            current_score = room[0].score
            room_id = room[0].id
            cache.set(str(room_id) + "__score", current_score, timeout=60 * 5)
            my_list = []
            # got room get question from it
            question = QuestionsModel.objects.filter(id=question_id)
            if not question.exists():
                return Response(status=400)
            # get testcases now
            test_cases = TestCaseHolder.objects.filter(question=question[0]).filter(is_sample=False)
            time_limit = getTimeLimit(language_id)
            BASE_URL = settings.HOST_URL + "/participant/callback/" + id + "/"
            current_code = base64.b64encode(current_code.encode("ascii")).decode("ascii")

            for i in test_cases:
                my_list.append({
                    "language_id": language_id,
                    "source_code": current_code,
                    "stdin": dobase64encode(i.stdin),
                    "expected_output": dobase64encode(i.stdout),
                    "memory_limit": i.max_memory * 1024,
                    "callback_url": BASE_URL + str(i.id),
                    "cpu_time_limit": time_limit * float(i.max_time),
                })
                # make data for sending it xD
            data = {
                "submissions": my_list
            }
            status, tokens = sendRequest(data, id, len(my_list))
            return Response({
                'status': status,
                'tokens': tokens
            }, status=200)


class CheckSubmissions(APIView):
    permission_classes = [IsnotDisqualified]
    parsers = [JSONParser]

    def post(self, request):
        try:
            id = request.data["id"]
            question_id = request.data["question_id"]
            room_seat = request.data["room_seat"]
        except:
            return Response(status=400)
        total_rooms = RoomParticipantAbstract.objects.all()
        room = total_rooms.filter(id=room_seat)
        if not room.exists():
            print("a")
            return Response(status=400)
        else:
            room = room[0]
            question = QuestionsModel.objects.filter(id=question_id)
            if not question.exists():
                print("b")
                return Response(status=400)
            allseat = RoomParticipantManager.objects.prefetch_related('room_seat').all()  # room_seat
            seat = allseat.filter(room_seat=room).filter(id=id)
            if not seat.exists():
                print("c")
                return Response(status=400)
            seat = seat[0]
            # Testcases
            root_testcases = TestCaseHolder.objects.filter(question=question[0].id).filter(is_sample=False)
            testcases = TestCaseSolutionLogger.objects.filter(room_solution=seat).filter(is_solved=True)
            testcases_solved = testcases.count()
            testcases_score = testcases.aggregate(Sum('score_for_this_testcase'))["score_for_this_testcase__sum"]
            print("TestCases Solved :", str(testcases_solved))
            total_testcases = root_testcases.count()
            # duration calculation
            duration = (seat.end_time - seat.start_time)
            duration_in_s = duration.total_seconds()
            duration_in_m = divmod(duration_in_s, 60)[0]
            score_reduction = (duration_in_m * settings.TIME_MULTIPLY_CONSTANT)
            print(testcases_score)
            print(score_reduction)
            try:
                total_score = math.ceil((testcases_score - score_reduction))
            except TypeError as e:
                print(e)
                total_score = 0
            previous_score = int(cache.get(str(seat.id) + "__score"))
            if previous_score > total_score:
                seat.score = previous_score
            else:
                seat.score = total_score
            test_cases_info = TestCasesSolutionSerailizer(testcases, many=True)

            if testcases_solved == total_testcases:
                seat.is_submitted = True

                seat.save()
                return Response({
                    'status': 'All test cases passed',
                    'testcases': testcases_solved,
                    'info': test_cases_info.data,
                    "total_questions_score": testcases_score,
                    "total_time": duration_in_m,
                    "time_score_reduction": score_reduction,
                    "overallstatus": "Please wait till the round ends!"
                }, status=200)

            else:
                seat.save()
                if testcases_solved == 0:
                    return Response({
                        'status': 'Failed!',
                        'testcases': testcases_solved,
                        'info': test_cases_info.data,
                        "total_questions_score": testcases_score,
                        "testcases_left": total_testcases - testcases_solved,
                        "total_time": duration_in_m,
                        "time_score_reduction": score_reduction,
                        "overallstatus": "None of the testcases passed!"
                    }, status=206)
                else:
                    return Response({
                        'status': 'Partially solved',
                        'testcases': testcases_solved,
                        'info': test_cases_info.data,
                        "total_questions_score": testcases_score,
                        "testcases_left": total_testcases - testcases_solved,
                        "total_time": duration_in_m,
                        "time_score_reduction": score_reduction,
                        "overallstatus": "Partially Solved!"
                    }, status=206)


class CheckSubmissionsAlreadySubmitted(APIView):
    permission_classes = [IsnotDisqualified]
    parsers = [JSONParser]

    def post(self, request):
        try:
            id = request.data["id"]
            room_seat = request.data["room_seat"]
        except:
            return Response(status=400)
        total_rooms = RoomParticipantAbstract.objects.all()
        room = total_rooms.filter(id=room_seat)
        if not room.exists():
            print("a")
            return Response(status=400)
        else:
            room = room[0]

            allseat = RoomParticipantManager.objects.prefetch_related('room_seat').all()  # room_seat
            seat = allseat.filter(room_seat=room).filter(id=id)
            if not seat.exists():
                print("c")
                return Response(status=400)

            # Testcases
            testcases = TestCaseSolutionLogger.objects.filter(room_solution=seat).filter(is_solved=True)
            testcases_score = testcases.aggregate(Sum('score_for_this_testcase'))["score_for_this_testcase__sum"]
            test_cases_info = TestCasesSolutionSerailizer(testcases, many=True)
            return Response({
                'info': test_cases_info.data,
                'total_score': testcases_score
            }, status=200)
