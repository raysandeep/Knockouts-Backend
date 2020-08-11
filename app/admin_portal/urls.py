from django.urls import path
from . import  views
urlpatterns = [
    path('question/get', views.QuestionsListAPIView.as_view()),
    path('question/update/<pk>', views.QuestionUpdateAPIView.as_view()),
    path('question/create', views.QuestionCreateAPIView.as_view()),
    path('testcase/get/<question>', views.TestCasesListAPIView.as_view()),
    path('testcase/update/<pk>', views.TestCaseUpdateAPIView.as_view()),
    path('testcase/create', views.TestCaseCreateAPIView.as_view()),
    path('rounds/get', views.RoundListAPIView.as_view()),
    path('rounds/update/<pk>', views.RoundUpdateAPIView.as_view()),
    path('rounds/create', views.RoundCreateAPIView.as_view()),
    path('assign',views.AssignPeopleAPIView.as_view()),
    path('rooms/list/<round>',views.GetAllRoomsListAPIView.as_view()),
    path('rooms/unassigned/<round>',views.GetPendingPplAPIView.as_view()),
    path('rooms/create',views.RoomCreateAPIView.as_view()),
    path('room/view/<pk>',views.RoomRetrieveAPIView.as_view()),
    path('room/destory/<pk>',views.RoomDestroyAPIView.as_view())
]
