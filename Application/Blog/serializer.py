from django.utils import timezone
from rest_framework import serializers
from Application.Blog.models import Blog
from Application.utils.custom_serializer import ModelSerializer
from Application.utils.custom_serializer_fields import StandardDateTimeField


class BlogsSerializer(ModelSerializer):
    id = serializers.IntegerField(label='id', read_only=True)
    title = serializers.CharField(required=True, label='标题', max_length=100)
    content = serializers.CharField(required=True, label='内容')
    type = serializers.IntegerField(required=True, label='文章类型')
    created_time = StandardDateTimeField(label='创建时间', read_only=True)
    updated_time = StandardDateTimeField(label='更新时间', read_only=True)

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


class BlogsListSerializer(ModelSerializer):

    class Meta:
        model = Blog
        exclude = ['content']
