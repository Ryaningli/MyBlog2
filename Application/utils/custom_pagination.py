import math
from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPageNumberPagination(PageNumberPagination):
    """
    自定义分页器
    """
    page_size_query_param = 'pagesize'

    def get_paginated_response(self, data):
        count = self.page.paginator.count
        pagesize = self.get_page_size(self.request)
        page_count = math.ceil(count / pagesize)

        return Response(OrderedDict([
            ('count', count),
            ('current_page', self.get_page_number(self.request, self)),
            ('page_count', page_count),
            ('pagesize', pagesize),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))
