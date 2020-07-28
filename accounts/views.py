from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser

from admin_portal.permissions import IsDSCQuestionModerator
from .serializers import (
    UserSignupSerializer,
    ProfilePicSerializer
)
from .models import (
    User,
    ProfilePic
)
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


# Create your views here.
class UserSignupView(APIView):
    permission_classes = (AllowAny,)
    parser_classes = [JSONParser]

    # Sigup user (create new object)
    def post(self, request):

        serializer = UserSignupSerializer(data=request.data)

        if serializer.is_valid():
            user_data = serializer.data
            try:
                User.objects.create_user(
                    password=user_data['password'],
                    username=user_data['username'],
                    phone=user_data['phone'],
                    full_name=user_data['full_name']
                )
            except ValueError as e:
                print(e)
                return Response({
                    'status': 'failed',
                    'error': str(e)
                }, status=403)
            return Response({"message": "User Signed up successfully"}, status=201)
        else:
            return Response({"message": serializer.errors}, status=400)


class UserLoginView(APIView):
    permission_classes = (AllowAny,)
    parser_classes = [JSONParser]

    # User Login Create a Auth Token
    def post(self, request):
        req_data = request.data
        user = authenticate(username=req_data['username'], password=req_data['password'])
        if not user:
            return Response({"message": "Invalid Details"}, status=400)
        elif user.is_blocked or user.is_disqualified:
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

    def post(self, request):
        req_data = request.data
        if not req_data['email']:
            return Response(status=403)
        user = User.objects.filter(username=req_data['email'])
        if user.count() == 1:
            user[0].is_disqualified = True
            return Response(status=204)
        return Response(status=403)


