from django.conf import settings
from django.contrib import auth
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from rest_framework import status
from rest_framework.authtoken import serializers
from rest_framework.authtoken.models import Token
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

    @staticmethod
    def post(request):
        serializer = serializer_list.LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = auth.authenticate(**serializer.data)
            if user:
                # auth.login(request, user)
                token, created = Token.objects.update_or_create(user=user)
                return Response(data=serializer.response(msg='登录成功', data={'Authorization': ' Token ' + token.key}))
            else:
                return Response(data=serializer.response(msg='用户名或密码错误'), status=status.HTTP_403_FORBIDDEN)
        return Response(data=serializer.response())


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)