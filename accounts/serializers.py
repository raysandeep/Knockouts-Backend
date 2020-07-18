from rest_framework import serializers
from .models import (
    User,
    ProfilePic
    )
from rest_framework.fields import CurrentUserDefault

class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ( 'username', 'full_name','phone', 'password')


class ProfilePicSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilePic
        fields = ['picture']