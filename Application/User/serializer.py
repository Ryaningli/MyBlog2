from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_jwt.serializers import jwt_payload_handler
from rest_framework_jwt.utils import jwt_encode_handler
from Application.User.models import User
from Application.utils import custom_serializer


class LoginSerializer(custom_serializer.Serializer):

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


class RegisterSerializer(custom_serializer.ModelSerializer):
    username = serializers.CharField(required=True, label='用户名', min_length=4, max_length=20,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message='用户名已存在')],
                                     error_messages={'required': '用户名不可为空'})
    password = serializers.CharField(required=True, label='密码', min_length=6, max_length=18,
                                     error_messages={'required': '密码不可为空'})
    email = serializers.EmailField(required=True, label='邮箱')

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'date_joined']

    def create(self, validated_data):
        validated_data['date_joined'] = timezone.now()
        user = User.objects.create_user(**validated_data)
        return validated_data


class UserInfoDetailSerializer(custom_serializer.ModelSerializer):

    password = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    @staticmethod
    def get_password(obj):
        return '******'
