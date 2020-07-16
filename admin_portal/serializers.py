from rest_framework import serializers

from .models import(
    QuestionsModel
)

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionsModel
        fields = [
            'question_title',
            'question',
            'difficulty_level'
        ]