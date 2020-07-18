from rest_framework import serializers

from .models import(
    QuestionsModel,
    TestCaseHolder,
    Rounds
)

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionsModel
        fields = [
            'question_title',
            'question',
            'difficulty_level',
            'id'
        ]

class AdminQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionsModel
        exclude = ['is_assigned']

class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCaseHolder
        fields = '__all__'
    
class RoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rounds
        fields = '__all__'
