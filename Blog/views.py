from django.contrib import auth
from rest_framework import status
from rest_framework.authtoken import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from Blog.models import User
from Blog import serializer as serializer_list


class ManageUser(APIView):
    def get(self, request, *args, **kwargs):
        users = serializer_list.UserSerializer(User.objects.all(), many=True).data
        return Response(users)


class Register(APIView):
    def get(self, request):
        return Response({'method': 'GET'})

    @staticmethod
    def post(request):
        serializer = serializer_list.RegisterSerializer(data=request.data)
        if serializer.is_valid():
            User.objects.create_user(**serializer.data)
            return Response(data=serializer.response())
        return Response(data=serializer.response())


class Login(APIView):
    def post(self, request):
        serializer = serializer_list.LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = auth.authenticate(**serializer.data)
            if user:
                auth.login(request, user)
                return Response(data=serializer.response(msg='登录成功', data=serializer.data))
            else:
                return Response(data=serializer.response(msg='用户名或密码错误'))
        return Response(data=serializer.response())