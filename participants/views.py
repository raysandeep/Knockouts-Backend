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
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from django.conf import settings


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
    for i in SAMPLE_JSON:
        if i["id"] == id:
            return i["time"]

    return 2.5

def sendRequest(data,room_id):
    headers = {
        'Content-Type': 'application/json'
        }
    response = rq.request("POST", settings.JUDGEAPI_URL, headers=headers, json = data)
    tokens = ''
    if response.status_code == 201:
        for i in response.json():
            tokens += i["token"] + ','
        tokens = tokens[:-1]
        print(tokens)
        if sendFastAPITrigger(room_id,tokens):
            return True,tokens
    return False,''


def sendFastAPITrigger(room_name):
    headers = {
        'Content-Type': 'application/json'
        }
    response = rq.request("GET", settings.FASTAPI_URL+'trigger/'+room_name+'/'+tokens)
    if response.status_code == 200:
        return True
    return False

def sendFastAPITriggerforproblem(room_name,token,status):
    headers = {
        'Content-Type': 'application/json'
        }
    response = rq.request("GET", settings.FASTAPI_URL+'trigger1/'+room_name+'/'+token+'/'+status)
    if response.status_code == 200:
        return True
    return False

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
    permission_classes = [IsAuthenticatedOrReadOnly]
    parsers = [JSONParser]



class TestCaseSolutionLogger(RetrieveAPIView):
    queryset = QuestionsModel.objects.all()
    permission_classes = [IsAdminUser]
    parsers = [JSONParser]
    serializer_class = QuestionAdminSerializer

class IntiateSubmitQuestion(APIView):
    def get(self,request,id):
        testcases = TestCaseSolutionLogger.objects.prefetch_related('participant').filter(room_solution=id).filter(participant=request.user)
        testcases.delete()
        return Response(status=204)
        
class CallBackHandler(APIView):
    def put(self,request,roomabsid,testid):
        data = request.data
        room = RoomParticipantAbstract.objects.filter(id=roomabsid)
        test_case = TestCaseHolder.objects.filter(id=testid)
        status=False
        if data['status']['id'] == 3:
            status = True
        
        dicti = {
            'room_solution':room[0],
            'test_case':test_case[0],
            'stdin':test_case[0].stdin,
            'stdout':data['stdout'],
            'time':data['time'],
            'memory':data['memory'],
            'error':data['compile_output'],
            'token':data['token'],
            'is_solved':status
        }
        testcase = TestCaseSolutionLogger(**dicti)
        testcase.save()

        sendFastAPITriggerforproblem(roomabsid,data['token'],status)
        pass

class SubmitQuestion(APIView):
    def post(self,request):
        try:
            id = request.data["id"]
            question_id = request.data["question_id"]
        except:
            return Response(status=400)
        #get room
        room = RoomParticipantAbstract.objects.filter(id=id)
        if not room.exists():
            return Response(status=400)
        else:
            #get code 
            language_id = room[0].language_of_code
            current_code = room[0].current_code
            my_list=[]
            #got room get question from it 
            question = QuestionsModel.objects.filter(id=question_id)
            if not question.exists():
                return Response(status=400)
            #get testcases now
            test_cases = TestCaseHolder.objects.filter(question=question[0])
            time_limit = getTimeLimit(language_id)
            BASE_URL = settings.HOST_URL+"/participant/callback/"+id+"/"
            for i in test_cases:
                my_list.append({
                    "lanuguage_id":language_id,
                    "source_code":current_code,
                    "stdin":i.stdin,
                    "expected_output":i.stdout,
                    "memory_limit":i.memory,
                    "callback_url":BASE_URL+i.id,
                    "cpu_time_limit":time_limit*i.max_time,
                })      
            #make data for sending it xD
            data = {
                "submissions":my_list
                }
            sendRequest(data,id)
            return Response({
                'status':'Started Submission'
            },status=200)

