from rest_framework import serializers

from admin_portal.models import(
    RoomParticipantAbstract,
    RoomParticipantManager
)


class RoomParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomParticipantManager
        fields = '__all__'


class RoomParticipantUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomParticipantManager
        exclude = ['end_time','start_time','is_submitted','score']

class RoomParticipantAbstractSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='participant.first_name')
    last_name = serializers.CharField(source='participant.last_name')
    participant_email = serializers.EmailField(source='participant.email')
    qualification = serializers.EmailField(source='participant.is_disqualified')
    block = serializers.EmailField(source='participant.is_blocked')
    currentStatus = serializers.SerializerMethodField()

    class Meta:
        model = RoomParticipantAbstract
        exclude = ['room']
        depth = 1

    def get_currentStatus(self, obj):
        return RoomParticipantSerializer(RoomParticipantManager.objects.filter(room_seat=obj.id), many=True).data
