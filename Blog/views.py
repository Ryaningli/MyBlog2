from django.shortcuts import render

# Create your views here.
from rest_framework.authtoken import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from Blog.models import User
from Blog.serializer import UserSerializer, RegisterSerializer


class ManageUser(APIView):
    def get(self, request, *args, **kwargs):
        users = UserSerializer(User.objects.all(), many=True).data
        return Response(users)


class Register(APIView):
    def get(self, request):
        return Response({'method': 'GET'})

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        print(request.data)
        print(serializer.is_valid())
        print(serializer.errors)
        # User.objects.create_user(username=request.data['username'], email=request.data['email'], password=request.data['password'])
        return Response({'msg': '处理成功'})
