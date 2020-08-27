from django.db import models
from uuid import uuid4
from django.contrib.postgres.fields import JSONField
from accounts.models import User
from . import default_json


class QuestionsModel(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    question_title = models.CharField(max_length=200)
    question = JSONField()
    is_assigned = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    difficulty_level = models.IntegerField(default=0)

    def __str__(self):
        return self.question_title


class TestCaseHolder(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    question = models.ForeignKey(QuestionsModel, on_delete=models.CASCADE)
    is_sample = models.BooleanField(default=False)
    stdin = models.TextField()
    stdout = models.TextField()
    max_time = models.DecimalField(max_digits=10, decimal_places=8)
    max_memory = models.IntegerField(default=0)
    score = models.IntegerField(default=10)


class Rounds(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    round_name = models.CharField(max_length=100)
    difficulty_allowance = models.IntegerField(default=0)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


class Rooms(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    question = models.OneToOneField(QuestionsModel, on_delete=models.CASCADE)
    round = models.ForeignKey(Rounds, on_delete=models.CASCADE)


# RoomParticipantAbstract Table
class RoomParticipantAbstract(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    participant = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "{} {}".format(self.participant.username, self.room.question.question_title)


class RoomParticipantManager(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    room_seat = models.OneToOneField(RoomParticipantAbstract, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now=True)
    current_code = models.TextField()
    language_of_code = models.CharField(max_length=100)
    is_submitted = models.BooleanField(default=False)
    score = models.IntegerField(default=0)

    def __str__(self):
        return "{} - {} - {}".format(self.room_seat.participant, self.is_submitted, self.score)


class TestCaseSolutionLogger(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    room_solution = models.ForeignKey(RoomParticipantManager, on_delete=models.CASCADE)
    test_case = models.ForeignKey(TestCaseHolder, on_delete=models.CASCADE)
    stdin = models.TextField(null=True)
    stdout = models.TextField(null=True)
    time = models.DecimalField(max_digits=10, decimal_places=8, null=True)
    memory = models.IntegerField(default=0, null=True)
    error = models.CharField(max_length=500, null=True)
    token = models.CharField(max_length=100)
    is_solved = models.BooleanField(default=False)
    score_for_this_testcase = models.IntegerField(default=0)


class DisQualifyModel(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    dis_round = models.ForeignKey(Rounds, on_delete=models.CASCADE)
    users = JSONField()


# 8
# Day 3 - 34 - 16
# 4 - 16 - 8
# 5 - 8 - 4
# 6 - 4 - 2
# 7 - 2 - 1