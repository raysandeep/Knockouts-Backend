from django.shortcuts import render
from rest_framework.generics import CreateAPIView,RetrieveUpdateDestroyAPIView,ListAPIView
from .permissions import IsDSCModerator,IsDSCQuestionModerator
from .models import (
    QuestionsModel,
    TestCaseHolder,
    Rounds
)
from .serializers import(
    QuestionSerializer,
    TestCaseSerializer,
    AdminQuestionSerializer,
    RoundSerializer,
)
from rest_framework.parsers import JSONParser


class QuestionCreateAPIView(CreateAPIView):
    queryset = QuestionsModel.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsDSCModerator]
    parsers = [JSONParser]


class QuestionUpdateAPIView(RetrieveUpdateDestroyAPIView):
    queryset = QuestionsModel.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsDSCQuestionModerator]
    parsers = [JSONParser]

    def get_serializer_class(self):
        if self.request.user.is_admin and self.request.user.is_staff:
            return AdminQuestionSerializer
        return QuestionSerializer


class QuestionsListAPIView(ListAPIView):
    queryset = QuestionsModel.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsDSCModerator]
    parsers = [JSONParser]


class TestCaseCreateAPIView(CreateAPIView):
    queryset = TestCaseHolder.objects.all()
    serializer_class = TestCaseSerializer
    permission_classes = [IsDSCModerator]
    parsers = [JSONParser]

class TestCasesListAPIView(ListAPIView):
    lookup_url_kwarg = "question"
    serializer_class = TestCaseSerializer
    permission_classes = [IsDSCModerator]
    parsers = [JSONParser]
    
    def get_queryset(self):
        question_id = self.kwargs.get(self.lookup_url_kwarg)
        testcase_list = TestCaseHolder.objects.filter(question=question_id)
        return testcase_list

class TestCaseUpdateAPIView(RetrieveUpdateDestroyAPIView):
    queryset = TestCaseHolder.objects.all()
    serializer_class = TestCaseSerializer
    permission_classes = [IsDSCQuestionModerator]
    parsers = [JSONParser]

class RoundCreateAPIView(CreateAPIView):
    queryset = Rounds.objects.all()
    serializer_class = RoundSerializer
    permission_classes = [IsDSCQuestionModerator]
    parsers = [JSONParser]


class RoundUpdateAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Rounds.objects.all()
    serializer_class = RoundSerializer
    permission_classes = [IsDSCQuestionModerator]
    parsers = [JSONParser]


class RoundListAPIView(ListAPIView):
    queryset = Rounds.objects.all()
    serializer_class = RoundSerializer
    permission_classes = [IsDSCQuestionModerator]
    parsers = [JSONParser]