from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import serializers
from rest_framework_jwt.serializers import jwt_payload_handler
from rest_framework_jwt.utils import jwt_encode_handler

from Application.User.models import User
from Application.utils.custom_base_serializer import Serializer


class LoginSerializer(Serializer):

    username = serializers.CharField(required=True, label='用户名', error_messages={'required': '用户名不可为空'})
    password = serializers.CharField(required=True, label='密码', error_messages={'required': '密码不可为空'})

    def validate(self, attrs):
        credentials = {
            'username': attrs.get('username'),
            'password': attrs.get('password')
        }

        if all(credentials.values()):
            user = authenticate(**credentials)

            if user:
                if not user.is_active:
                    msg = '用户已被禁用'
                    raise serializers.ValidationError(msg)

                payload = jwt_payload_handler(user)
                user.last_login = timezone.now()
                user.save()
                return {
                    'token': jwt_encode_handler(payload),
                    'user': user
                }
            else:
                msg = '用户名或密码错误'
                raise serializers.ValidationError(msg)


class TestSerializer(Serializer):
    test = serializers.CharField(required=True, error_messages={'required': 'test不可为空'})

    def validate(self, attrs):
        return {'t1': attrs.get('test'), 't2': 2}
