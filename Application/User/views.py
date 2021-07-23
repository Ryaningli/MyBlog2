from django.shortcuts import render

from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

from Application.User.models import User
from Application.User.serializer import LoginSerializer, RegisterSerializer
from Application.utils.resopne_data import ResponseData


class Login(APIView):

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid()
        data = serializer.validated_data
        user = serializer.validated_data['user']
        data['user'] = user.username
        return Response(data=ResponseData(data=data, msg='登录成功'))


class Register(APIView):

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid()
        user = serializer.create(serializer.data)
        if user:
            return Response(ResponseData(msg='注册成功', data=user,
                                         date_joined=User.objects.get(username=user['username']).date_joined))
