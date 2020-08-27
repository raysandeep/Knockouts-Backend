import csv

from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from accounts.models import User
from admin_portal.models import (
    Rounds,
    RoomParticipantAbstract,
    Rooms,
    RoomParticipantManager,
    TestCaseSolutionLogger,
    TestCaseHolder,
    QuestionsModel
)


class Health(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response(status=204)


def download_csv(request, queryset):
    opts = queryset.model._meta
    model = queryset.model
    response = HttpResponse()
    response['Content-Disposition'] = 'attachment;filename=export.csv'
    writer = csv.writer(response)
    field_names = [field.name for field in opts.fields]
    writer.writerow(field_names)
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])
    return response


def myview(request):
    data = download_csv(request, User.objects.filter(is_disqualified=True))

    return HttpResponse(data, content_type='text/csv')


class ScoreCount(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        room = Rooms.objects.filter(round="bc901620-00e6-438a-b254-f52177635faa")
        room_abstract = RoomParticipantAbstract.objects.all()
        room_managers = RoomParticipantManager.objects.all()
        testcases = TestCaseHolder.objects.all()
        questions = QuestionsModel.objects.filter(is_assigned=True)
        testcases_solution = TestCaseSolutionLogger.objects.all()
        main_list = []
        qualified = []
        disqualified = []
        tied = []
        for i in room:
            room_abstract_of_users = room_abstract.filter(room=i.id)
            room_list = []

            # get room
            question_for_room = questions.filter(id=i.question.id)
            if not question_for_room.exists():
                print("error no question exisits")
                print("room : ", i.id)
            else:
                question_for_room = question_for_room[0]

            # get testcases count
            testcases_count = testcases.filter(question=question_for_room.id)
            testcases_count = testcases_count.count()

            # rim
            for j in room_abstract_of_users:
                data = {
                    "user": j.participant.username,
                    "tescases_available": testcases_count,
                    "testcases_solved": 0,
                    "question": question_for_room.question_title,
                    "question_watched": True,
                    "status": "Disqualified",
                    "score": 0,
                    "time_taken": 0
                }
                room_seat = room_managers.filter(room_seat=j.id)
                if room_seat.exists():
                    testcases_solved = testcases_solution.filter(room_solution=room_seat[0].id).filter(is_solved=True)
                    testcases_solved = testcases_solved.count()
                    data['testcases_solved'] = testcases_solved
                    duration = (room_seat[0].end_time - room_seat[0].start_time)
                    duration_in_s = duration.total_seconds()
                    duration_in_m = divmod(duration_in_s, 60)[0]
                    data['time_taken'] = duration_in_m
                    data['score'] = room_seat[0].score
                else:
                    data['question_watched'] = False
                print(data)

                room_list.append(data)
            room_list = sorted(room_list, key=lambda elem: elem['testcases_solved'], reverse=True)
            if room_list[0]['testcases_solved'] > 0:
                room_list[0]['status'] = "Qualified"
                qualified.append(room_list[0]['user'])

                highesht_ts = room_list[0]['testcases_solved']
            else:
                highesht_ts = 0
            for i in range(1, len(room_list)):
                if highesht_ts == room_list[i]['testcases_solved'] and highesht_ts != 0:

                    tied.append(room_list[0]['user'])
                    tied.append(room_list[i]['user'])
                    try:
                        qualified.remove(room_list[0]['user'])
                    except:
                        pass

                else:
                    disqualified.append(room_list[i]['user'])

            main_list.append(room_list)
        return Response({
            "qualified": qualified,
            "len1": len(qualified),
            "disqualified": disqualified,
            "len2": len(disqualified),
            "tied": tied,
            "len3": len(tied),
            "main": main_list
        })
