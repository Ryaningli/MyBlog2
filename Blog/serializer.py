from rest_framework import serializers

from Blog.models import User


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    last_login = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = User
        fields = '__all__'


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, label='用户名', min_length=4, max_length=10, error_messages={
        'required': '用户名不可为空'
    })
    password = serializers.CharField(required=True, min_length=6, max_length=18)

    # class Meta:
    #     model = User
    #     fields = ['username', 'email', 'password']


