from django.urls import path
from . import  views
urlpatterns = [
    path('dash',views.DashBoardListAPIView.as_view()),
    path('code/view/<str:pk>',views.CodeRetrieveAPIView.as_view()),
    path('code/update',views.CodeCreateAPIView.as_view())
]