from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.authtoken import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from Blog.models import User
from Blog.serializer import UserSerializer, RegisterSerializer, TestSerializer
from Blog.utils.data_factory import ResponseData


class ManageUser(APIView):
    def get(self, request, *args, **kwargs):
        users = UserSerializer(User.objects.all(), many=True).data
        return Response(users)


class Register(APIView):
    def get(self, request):
        return Response({'method': 'GET'})

    @staticmethod
    def post(request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            User.objects.create_user(**serializer.data)
            return Response(ResponseData().SUCCESS)
        return Response(ResponseData(msg=serializer.error).BAD_REQUEST_PARAMETER, status=status.HTTP_201_CREATED)


class Test(APIView):
    @staticmethod
    def post(request):
        serializer = TestSerializer(data=request.data)
        print(serializer.is_valid())
        # print(serializer.errors)
        # print(serializer['fie'].label)
        print(serializer.error)
        return Response()
