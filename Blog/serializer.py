from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from Blog.models import User, Blog
from django.contrib import auth


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    last_login = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = User
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, label='用户名',
                                     validators=[UniqueValidator(queryset=User.objects.all(), message='用户名已存在')],
                                     min_length=4,
                                     max_length=10)
    password = serializers.CharField(required=True, label='密码', min_length=6, max_length=18)
    email = serializers.EmailField(required=True, label='电子邮箱')

    class Meta:
        model = User
        fields = ['username', 'password', 'email']


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, label='用户名', error_messages={'required': '用户名不可为空'})
    password = serializers.CharField(required=True, label='密码', error_messages={'required': '密码不可为空'})

    class Meta:
        model = User
        fields = ['username', 'password']

    def validate(self, attrs):
        user = auth.authenticate(username=attrs.get('username'), password=attrs.get('password'))
        if user:
            return user
        else:
            raise serializers.ValidationError('用户名或密码错误！')


class ManageBlogsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(label='id', read_only=True)
    title = serializers.CharField(required=True, label='标题', max_length=100)
    content = serializers.CharField(required=True, label='内容')
    type = serializers.IntegerField(required=True, label='文章类型')
    created_time = serializers.DateTimeField(label='创建时间', read_only=True, format='%Y-%m-%d %H:%M:%S')
    updated_time = serializers.DateTimeField(label='更新时间', read_only=True, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Blog
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        return Blog.objects.create(**validated_data, created_time=timezone.now(), user_id=user.id)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.type = validated_data.get('type', instance.type)
        instance.updated_time = timezone.now()
        instance.save()
        return instance
