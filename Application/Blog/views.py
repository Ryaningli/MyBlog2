from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from Application.Blog.models import Blog
from Application.Blog.serializer import BlogsSerializer, BlogsListSerializer
from Application.utils.custom_authentication import JSONWebTokenAuthentication


class Blogs(ModelViewSet):
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = Blog.objects.all()
    # serializer_class = BlogsSerializer
    # permission_classes = [IsAdminUser]

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
