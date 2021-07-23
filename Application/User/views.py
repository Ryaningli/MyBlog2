from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from Application.User.serializer import LoginSerializer, TestSerializer


class Login(APIView):

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid()
        data = serializer.validated_data
        user = serializer.validated_data['user']
        data['user'] = user.username
        return Response(data=data)


class Test(APIView):

    def post(self, request):
        serializer = TestSerializer(data=request.data)
        result = serializer.is_valid(raise_exception=True)
        print(result)
        data = serializer.validated_data
        print(type(data))
        return Response(data={'data': '测试'})