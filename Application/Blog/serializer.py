from django.utils import timezone
from rest_framework import serializers
from rest_framework import filters
from Application.Blog.models import Blog, Comment
from Application.User.models import User
from Application.utils.custom_serializer import ModelSerializer


class UserInfoSerializer(ModelSerializer):
    """
    通用用户信息序列化类
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'nick_name')


class BlogsSerializer(ModelSerializer):
    """
    日志序列化类
    """
    id = serializers.IntegerField(label='id', read_only=True)
    title = serializers.CharField(required=True, label='标题', max_length=100)
    content = serializers.CharField(required=True, label='内容')
    type = serializers.IntegerField(required=True, label='文章类型')
    user = UserInfoSerializer(read_only=True)

    class Meta:
        model = Blog
        fields = '__all__'
        read_only_fields = ['created_time', 'updated_time']

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
    """
    日志列表序列化类
    """
    user = UserInfoSerializer(read_only=True)

    class Meta:
        model = Blog
        exclude = ['content']


class CommentSerializer(ModelSerializer):
    """
    评论序列化类
    """
    object_id = serializers.IntegerField(required=True, label='评论对象id', write_only=True)
    level = serializers.IntegerField(required=True, label='评论等级')
    state = serializers.IntegerField(label='状态', read_only=True)
    user = UserInfoSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['created_time', ]

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
        validated_data['level'] = attrs.get('level')
        return validated_data


class CommentListSerializer(ModelSerializer):
    """
    评论列表序列化类
    """
    user = UserInfoSerializer(read_only=True)
    content = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'

    @staticmethod
    def get_content(obj):
        """
        当state=0(被删除)时，隐藏评论内容
        """
        if obj.state == 0:
            obj.content = None
        return obj.content


class StandardCommentListSerializer(ModelSerializer):
    """
    规范后的评论列表序列化类
    """
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = '__all__'

    @staticmethod
    def comment_data_handler(data):
        """
        评论数据处理
        :param data:
        :return:
        """
        comment_list = []
        result = {
            'list': [],
            'count': 0
        }
        for value in data:
            if value['level'] == 1:
                comment_list.append([value, ])

        for idx, val in enumerate(comment_list):
            for value in data:
                if value['level'] == 2 and value['lv1_comment'] == val[0]['id']:
                    comment_list[idx].append(value)

        for value in comment_list:
            one_data = {
                'lv1': None,
                'lv2': [],
                'count': 0
            }
            for v in value:
                if v['level'] == 1:
                    one_data['lv1'] = v
                else:
                    one_data['lv2'].append(v)
            one_data['count'] = len(value)
            result['list'].append(one_data)

        result['count'] = len(data)
        return result

    def get_comments(self, obj):
        queryset = Comment.objects.filter(blog_id=obj.id)
        queryset = filters.OrderingFilter().filter_queryset(self.context['request'], queryset, self.context['view'])
        data = CommentListSerializer(queryset, many=True).data
        result = self.comment_data_handler(data)
        return result
