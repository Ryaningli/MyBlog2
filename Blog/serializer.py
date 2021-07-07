from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from Blog.models import User, Test
from Blog.utils.Serializer import Serializer, ModelSerializer


class UserSerializer(ModelSerializer):
    date_joined = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    last_login = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = User
        fields = '__all__'


class RegisterSerializer(ModelSerializer):
    username = serializers.CharField(required=True, label='用户名',
                                     validators=[UniqueValidator(queryset=User.objects.all(), message='用户名已存在')],
                                     min_length=4,
                                     max_length=10)
    password = serializers.CharField(required=True, label='密码', min_length=6, max_length=18)
    email = serializers.EmailField(required=True, label='电子邮箱')

    class Meta:
        model = User
        fields = ['username', 'password', 'email']


class TestSerializer(Serializer):
    fie = serializers.CharField(required=True, label='字段fie', min_length=4)
    test = serializers.CharField(required=True, label='测试')

    class Meta:
        model = Test
        fields = '__all__'
