from collections import OrderedDict

from rest_framework import filters, mixins
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from Application.Blog.filters import BlogsFilter, CommentFilter
from Application.Blog.models import Blog, Comment
from Application.Blog.serializer import BlogsSerializer, BlogsListSerializer, CommentSerializer, CommentListSerializer
from Application.utils.custom_permissions import IsOwner


class Blogs(ModelViewSet):
    queryset = Blog.objects.all().order_by('created_time').reverse()
    filter_backends = [filters.OrderingFilter]
    filter_class = BlogsFilter
    ordering_fields = ('id', 'title', 'created_time', 'user_id')

    def get_serializer_class(self):
        if self.action == 'list':
            return BlogsListSerializer
        else:
            return BlogsSerializer

    def get_permissions(self):
        if self.action in ['retrieve', 'list']:
            return []
        else:
            return [IsAdminUser()]

    # 根据user_id返回
    # def get_queryset(self):
    #     return self.queryset.filter(user_id=self.request.user.id)


class Comments(mixins.CreateModelMixin,
               mixins.DestroyModelMixin,
               mixins.RetrieveModelMixin,
               mixins.ListModelMixin,
               GenericViewSet):
    """
    创建评论: POST api/blog/comment/
    删除评论: DELETE api/blog/comment/{id}/
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_class = CommentFilter
    ordering_fields = ('created_time', )

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return []
        else:
            return [IsAuthenticated(), IsOwner()]

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

    def retrieve(self, *args, **kwargs):
        """
        未做分页
        :return: {
            'list': [{
                'lv1': '',
                'lv2': [],
                'count': 0
                }],
            'count': 0
        }
        """
        queryset = Comment.objects.filter(blog_id=kwargs['pk'])
        queryset = filters.OrderingFilter().filter_queryset(self.request, queryset, self)
        data = CommentListSerializer(queryset, many=True).data
        result = self.comment_data_handler(data)
        return Response(data=result)
