from rest_framework import serializers

from .models import(
    QuestionsModel,
    TestCaseHolder,
    Rounds,
    RoomParticipantAbstract,
    Rooms
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

class RoomParticipantAbstractSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='participant.full_name')
    room_question = serializers.CharField(source='room.question.id')
    participant_email = serializers.EmailField(source='participant.username')
    class Meta:
        model = RoomParticipantAbstract
        exclude = ['room']

class RoomsSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()
    class Meta:
        model = Rooms
        fields = '__all__'

    def get_participants(self, obj):
        return RoomParticipantAbstractSerializer(RoomParticipantAbstract.objects.filter(room=obj.id), many=True).data
