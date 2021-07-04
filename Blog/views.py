from django.shortcuts import render

# Create your views here.
from rest_framework.authtoken import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from Blog.models import User


class ManageUser(APIView):
    def get(self, request, *args, **kwargs):
        users = serializers.Us
        return Response(users)