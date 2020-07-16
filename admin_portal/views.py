from django.shortcuts import render
from rest_framework.generics import CreateAPIView,RetrieveUpdateAPIView,ListAPIView
from .permissions import IsDSCModerator
from .models import (
    QuestionsModel,
    TestCaseHolder
)
from .serializers import(
    QuestionSerializer
)
from rest_framework.parsers import JSONParser


class QuestionCreateAPIView(CreateAPIView):
    queryset = QuestionsModel.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsDSCModerator]
    parsers = [JSONParser]


class QuestionUpdateAPIView(RetrieveUpdateAPIView):
    queryset = QuestionsModel.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsDSCModerator]
    parsers = [JSONParser]



class QuestionsListAPIView(ListAPIView):
    queryset = QuestionsModel.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsDSCModerator]
    parsers = [JSONParser]
