from django.contrib import admin

# Register your models here.
from .models import (
    QuestionsModel,
    TestCaseHolder
)


admin.site.register(QuestionsModel)
admin.site.register(TestCaseHolder)
