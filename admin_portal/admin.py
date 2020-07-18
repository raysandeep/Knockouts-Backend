from django.contrib import admin

# Register your models here.
from .models import (
    QuestionsModel,
    TestCaseHolder,
    RoomParticipantAbstract,
    RoomParticipantManager,
    Rooms,
    Rounds
)


admin.site.register(QuestionsModel)
admin.site.register(TestCaseHolder)
admin.site.register(RoomParticipantAbstract)
admin.site.register(RoomParticipantManager)
admin.site.register(Rooms)
admin.site.register(Rounds)
