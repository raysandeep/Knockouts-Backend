from django.urls import path
from . import  views
urlpatterns = [
    path('question/get', views.QuestionsListAPIView.as_view()),
    path('question/update/<pk>', views.QuestionUpdateAPIView.as_view()),
    path('question/create', views.QuestionCreateAPIView.as_view())
]
