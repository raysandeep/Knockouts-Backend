from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser

from admin_portal.permissions import IsDSCQuestionModerator
from .serializers import (
    UserSignupSerializer,
    ProfilePicSerializer,
    UserAdminSerializer,
    SocialSerializer
)
from .models import (
    User,
    ProfilePic
)
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from social_django.utils import load_strategy, load_backend
from social_core.exceptions import MissingBackend, AuthTokenError, AuthForbidden
from social_core.backends.oauth import BaseOAuth2
from django.conf import settings
import requests
import random
import string


# Create your views here.
class UserSignupView(APIView):
    permission_classes = (AllowAny,)
    parser_classes = [JSONParser]

    def get_random_string(self, length):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        print("Random string of length", length, "is:", result_str)
        return result_str

    # Sigup user (create new object)
    def post(self, request):
        data = {
            'secret': settings.GOOGLE_RECAPTCHA,
            'response': request.data.get('g_token', None)
        }

        resp = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data=data
        )

        print(resp.json())

        if not resp.json().get('success'):
            return Response(data={'message': 'ReCAPTCHA not verified!'}, status=406)

        serializer = UserSignupSerializer(data=request.data)

        if serializer.is_valid():
            user_data = serializer.data
            password = request.data.get('password', self.get_random_string(8))
            try:
                User.objects.create_user(
                    password=password,
                    username=user_data['username'],
                    phone=user_data['phone'],
                    full_name=user_data['full_name']
                )
            except ValueError as e:
                print(e)
                return Response({
                    'message': 'Please don\'t try to override the config!',
                    'error': str(e)
                }, status=403)
            return Response({"message": "User Signed up successfully!"}, status=201)
        else:
            return Response({"message": "User already exists!", "errors": serializer.errors}, status=409)


class UserLoginView(APIView):
    permission_classes = (AllowAny,)
    parser_classes = [JSONParser]

    # User Login Create a Auth Token
    def post(self, request):
        data = {
            'secret': settings.GOOGLE_RECAPTCHA,
            'response': request.data.get('g_token', None)
        }

        resp = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data=data
        )

        print(resp.json())

        if not resp.json().get('success'):
            return Response(data={'message': 'ReCAPTCHA not verified!'}, status=406)

        password = request.data.get('password', None)
        print(password)

        if password == None:
            user = User.objects.filter(username=request.data['username'])
            print(user.count())
            if user.count() == 0:
                return Response({"message": "Invalid Details"}, status=400)
            user = user[0]
        else:
            user = authenticate(username=request.data['username'], password=password)
            print(user)
            if not user:
                return Response({"message": "Invalid Details"}, status=400)

        try:
            condition = user.is_blocked or user.is_disqualified
        except:
            pass

        if condition:
            return Response({"message": "You don't have access to the portal. Contact contact@dscvit.com"}, status=403)
        else:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "message": "User Logged In",
                "user": {
                    "username": user.username,
                    "full_name": user.full_name,
                    "phone_no": user.phone,
                    "token": token.key
                }}, status=200)


class AdminLoginView(APIView):
    permission_classes = (AllowAny,)
    parser_classes = [JSONParser]

    # User Login Create a Auth Token
    def post(self, request):
        data = {
            'secret': settings.GOOGLE_RECAPTCHA,
            'response': request.data.get('g_token', None)
        }

        resp = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data=data
        )

        print(resp.json())

        if not resp.json().get('success'):
            return Response(data={'message': 'ReCAPTCHA not verified!'}, status=406)

        req_data = request.data
        user = authenticate(username=req_data['username'], password=req_data['password'])
        if not user:
            return Response({"message": "Invalid Details"}, status=400)
        elif not user.is_admin:
            return Response({"message": "Invalid Details"}, status=400)
        else:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "message": "User Logged In",
                "user": {
                    "username": user.username,
                    "full_name": user.full_name,
                    "phone_no": user.phone,
                    "token": token.key
                }}, status=200)


class DisQualifyUser(APIView):
    permission_classes = [IsDSCQuestionModerator]

    def get(self, request):
        user = User.objects.filter(is_admin=False)
        serializer = UserAdminSerializer(user, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        req_data = request.data
        if not req_data['email']:
            return Response(status=403)
        user = User.objects.filter(username=req_data['email'])
        if user.count() == 1:
            user[0].is_disqualified = True
            return Response(status=204)
        return Response(status=403)


class Googlelogin(APIView):
    permission_classes = (AllowAny,)
    parser_classes = [JSONParser]

    def post(self, request):
        req_data = request.data
        serializer = SocialSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        provider = req_data['provider']
        strategy = load_strategy(request)

        try:
            backend = load_backend(
                strategy=strategy,
                name=provider,
                redirect_uri=None)
        except MissingBackend:
            return Response({"message": "Please provide a valid provider"}, status=400)

        try:
            if isinstance(backend, BaseOAuth2):
                access_token = req_data['access_token']

            # Creating a new user by using google or facebook
            user = backend.do_auth(access_token)
            print(user.id)
            authenticated_user = backend.do_auth(access_token, user=user)

        except Exception as error:
            return Response({
                "error": {
                    "access_token": "Invalid token",
                    "details": str(error)
                }
            }, status=400)

        if authenticated_user and authenticated_user.is_active:
            user = User.objects.filter(Q(username__iexact=user.username) & Q(email=user.email))
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "message": "User Logged In",
                "user": {
                    "username": user.username,
                    "full_name": user.full_name,
                    "phone_no": user.phone,
                    "token": token.key
                }}, status=200)
        else:
            return Response({
                'message': 'Failed'
            }, status=400)
