from django.urls import path
from . import  views
urlpatterns = [
    path('dash',views.DashBoardListAPIView.as_view()),
    path('code/view/<pk>',views.CodeRetrieveAPIView.as_view()),
    path('code/update',views.CodeCreateAPIView.as_view()),
    path('question/<pk>',views.QuestionAndTestCaseGETAPIView.as_view()),
    path('admin/code/view/<pk>',views.CodeRetrieveAPIView.as_view()),
    path('admin/testcase/view/<pk>',views.TestCaseAPIView.as_view()),   
]