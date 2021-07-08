from django.middleware.csrf import get_token
from django.utils.deprecation import MiddlewareMixin


class CsrfTokenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        get_token(request)
