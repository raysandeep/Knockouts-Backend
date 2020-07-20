from django.urls import path
from . import  views
urlpatterns = [
    path('dash',views.DashBoardListAPIView.as_view()),
    path('code/view/<pk>',views.CodeRetrieveAPIView.as_view()),
    path('code/update/<pk>',views.CodeUpdateAPIView.as_view())
]