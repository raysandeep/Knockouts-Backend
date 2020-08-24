from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import (
    User,
    ProfilePic
)
from rest_framework.fields import CurrentUserDefault
from django.utils.html import escape
import string


def filter(text):
    allowed = string.ascii_letters + string.digits
    text = str(text)
    for alphanumeric in text:

        if alphanumeric not in allowed:
            text = text.replace(alphanumeric, '')

    return text


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'full_name', 'phone')

    def validate(self, value):
        dicti = {
            'full_name': filter(value['full_name']),
            'username': value['username'],
            'phone': filter(value['phone'])
        }
        return dicti


class UserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'full_name', 'phone', 'is_disqualified', 'date_joined', 'last_login', 'is_blocked')

    def validate(self, value):
        return value


class ProfilePicSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilePic
        fields = ['picture']


class SocialSerializer(serializers.Serializer):
    provider = serializers.CharField(max_length=255, required=True)
    access_token = serializers.CharField(max_length=4096, required=True, trim_whitespace=True)
