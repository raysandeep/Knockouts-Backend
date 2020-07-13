from django.urls import path
from . import  views
urlpatterns = [
    path('signup', views.UserSignupView.as_view()),
    path('login', views.UserLoginView.as_view())
]
