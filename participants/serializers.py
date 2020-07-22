from rest_framework import serializers

from admin_portal.models import(
    RoomParticipantAbstract,
    RoomParticipantManager,
    QuestionsModel,
    TestCaseHolder
)

class TestCaseSerializer(serializers.ModelSerializer):
    testcases = serializers.SerializerMethodField()
    class Meta:
        model = TestCaseHolder
        exclude = ['question']

class QuestionSerializer(serializers.ModelSerializer):
    testcases = serializers.SerializerMethodField()
    class Meta:
        model = QuestionsModel
        fields = ['id','question_title','question']

    def get_testcases(self,obj):
        return TestCaseSerializer(TestCaseHolder.objects.filter(question=obj.id).filter(is_sample=True)).data

class RoomParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomParticipantManager
        fields = '__all__'


class RoomParticipantUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomParticipantManager
        exclude = ['end_time','start_time','is_submitted','score']

class RoomParticipantAbstractSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='participant.full_name')
    participant_email = serializers.EmailField(source='participant.username')
    qualification = serializers.BooleanField(source='participant.is_disqualified')
    block = serializers.BooleanField(source='participant.is_blocked')
    currentStatus = serializers.SerializerMethodField()

    class Meta:
        model = RoomParticipantAbstract
        exclude = ['participant']
        depth = 1

    def get_currentStatus(self, obj):
        return RoomParticipantSerializer(RoomParticipantManager.objects.filter(room_seat=obj.id), many=True).data



class QuestionAdminSerializer(serializers.ModelSerializer):
    testcases = serializers.SerializerMethodField()
    class Meta:
        model = QuestionsModel
        fields = ['id','question_title','question','testcases']

    def get_tescases(self,obj):
        return TestCaseSerializer(TestCaseHolder.objects.filter(question=obj.id)).data