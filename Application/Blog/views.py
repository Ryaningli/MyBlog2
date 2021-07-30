from rest_framework import filters, mixins
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from Application.Blog.filters import BlogsFilter, CommentFilter
from Application.Blog.models import Blog, Comment
from Application.Blog.serializer import BlogsSerializer, BlogsListSerializer, CommentSerializer
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
               mixins.ListModelMixin,
               GenericViewSet):
    """
    创建评论: POST api/blog/comment/
    删除评论: DELETE api/blog/comment/{id}/
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_class = CommentFilter

    def get_permissions(self):
        if self.action == 'list':
            return []
        else:
            return [IsAuthenticated(), IsOwner()]
