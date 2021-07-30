from django.utils import timezone
from rest_framework import serializers
from Application.Blog.models import Blog, Comment
from Application.User.models import User
from Application.utils.custom_serializer import ModelSerializer
from Application.utils.custom_serializer_fields import StandardDateTimeField


class BlogsSerializer(ModelSerializer):
    id = serializers.IntegerField(label='id', read_only=True)
    title = serializers.CharField(required=True, label='标题', max_length=100)
    content = serializers.CharField(required=True, label='内容')
    type = serializers.IntegerField(required=True, label='文章类型')
    created_time = StandardDateTimeField(label='创建时间', read_only=True)
    updated_time = StandardDateTimeField(label='更新时间', read_only=True)
    username = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = '__all__'

    @staticmethod
    def get_username(obj):
        user = User.objects.get(id=obj.user_id)
        return user.username

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


class BlogsListSerializer(ModelSerializer):
    class Meta:
        model = Blog
        exclude = ['content']


class CommentSerializer(ModelSerializer):
    blog = serializers.PrimaryKeyRelatedField(allow_empty=False, queryset=Blog.objects.all(), label='日志主键')
    parent = serializers.PrimaryKeyRelatedField(allow_empty=False, allow_null=True, queryset=Comment.objects.all(),
                                                required=False, label='父评论主键')
    created_time = StandardDateTimeField(label='评论时间', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        return Comment.objects.create(**validated_data, created_time=timezone.now(), user_id=user.id)
