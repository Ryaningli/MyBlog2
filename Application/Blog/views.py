from rest_framework import filters, mixins
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from Application.Blog.filters import BlogsFilter, CommentFilter
from Application.Blog.models import Blog, Comment
from Application.Blog.serializer import BlogsSerializer, BlogsListSerializer, CommentSerializer, \
    StandardCommentListSerializer, LikeSerializer
from Application.utils import custom_mixins
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

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views_count = instance.views_count + 1  # 访问量统计
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class Comments(mixins.CreateModelMixin,
               custom_mixins.FakeDestroyModelMixin,
               mixins.RetrieveModelMixin,
               mixins.ListModelMixin,
               GenericViewSet):
    """
    创建评论: POST api/blog/comment/
    删除评论: DELETE api/blog/comment/{id}/
    """
    queryset = Comment.objects.all()
    filter_class = CommentFilter
    ordering_fields = ('created_time',)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return []
        else:
            return [IsAuthenticated(), IsOwner()]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return StandardCommentListSerializer
        else:
            return CommentSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = Blog.objects.get(id=kwargs['pk'])
        except Blog.DoesNotExist:
            raise NotFound('未找到')
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class Likes(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        self.request.data['user_id'] = self.request.user.id
        serializer = LikeSerializer(data=self.request.data, context={'request': self.request})
        serializer.is_valid()

        return Response(data=serializer.create(serializer.validated_data))
