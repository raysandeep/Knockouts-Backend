from django.urls import path
from . import views

urlpatterns = [

    path('dash', views.DashBoardListAPIView.as_view()),
    path('code/view/<pk>', views.CodeRetrieveAPIView.as_view()),
    path('code/update', views.CodeCreateAPIView.as_view()),
    path('question/<pk>', views.QuestionAndTestCaseGETAPIView.as_view()),
    path('callback/<str:roomabsid>/<str:testid>', views.CallBackHandler.as_view()),
    path('submit', views.SubmitQuestion.as_view()),
    path('submit/validate/', views.CheckSubmissions.as_view()),
    path('submit/check/', views.CheckSubmissionsAlreadySubmitted.as_view())

]
