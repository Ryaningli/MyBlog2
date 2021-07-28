import django_filters

from Application.Blog.models import Blog


class BlogsFilter(django_filters.rest_framework.FilterSet):
    # title = django_filters.CharFilter(field_name='title', help_text='文章标题')
    # created_time = django_filters.DateTimeFilter(field_name='created_time', help_text='发布时间', lookup_expr='contains', label='adfsssssssssssss')

    class Meta:
        model = Blog
        # fields = ['title', 'content', 'created_time']
        # fields = {
        #     'created_time': ['contains', ]
        # }
        fields =