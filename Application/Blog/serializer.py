from django.utils import timezone
from rest_framework import serializers
from Application.Blog.models import Blog, Comment
from Application.User.models import User
from Application.utils.custom_serializer import ModelSerializer, Serializer
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
    object_id = serializers.IntegerField(required=True, label='评论对象id', write_only=True)
    level = serializers.IntegerField(required=True, label='评论等级')
    created_time = StandardDateTimeField(label='评论时间', read_only=True)
    state = serializers.IntegerField(label='状态', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        return Comment.objects.create(**validated_data, created_time=timezone.now(), user_id=user.id)

    def validate(self, attrs):
        """
        level==1 => blog_id = object_id
        level==2 => parent_id = object_id
        """
        object_id = attrs.get('object_id')
        level = attrs.get('level')
        validated_data = {}
        if level == 1:
            try:
                blog = Blog.objects.get(id=object_id)
                validated_data['blog_id'] = blog.id
            except Blog.DoesNotExist:
                raise serializers.ValidationError('日志不存在')
        elif level == 2:
            try:
                comment = Comment.objects.get(id=object_id)
                validated_data['blog_id'] = comment.blog_id
                validated_data['parent_id'] = comment.id
                validated_data['lv1_comment_id'] = comment.lv1_comment_id or comment.id
            except Comment.DoesNotExist:
                raise serializers.ValidationError('评论不存在')
        else:
            raise serializers.ValidationError('评论等级参数错误')
        validated_data['content'] = attrs.get('content')
        return validated_data


class CommentListSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
