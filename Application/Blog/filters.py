import django_filters
from django_filters.rest_framework import FilterSet

from Application.Blog.models import Blog, Comment


class BlogsFilter(FilterSet):
    title = django_filters.CharFilter(field_name='title', label='文章标题', lookup_expr='contains')
    content = django_filters.CharFilter(field_name='content', label='文章内容', lookup_expr='contains')
    create_time_gt = django_filters.DateTimeFilter(field_name='created_time', lookup_expr='gte')
    create_time_lt = django_filters.DateTimeFilter(field_name='created_time', lookup_expr='lte')

    class Meta:
        model = Blog
        fields = []


class CommentFilter(FilterSet):
    blog = django_filters.CharFilter(field_name='blog_id', label='日志主键')

    class Meta:
        model = Comment
        fields = []