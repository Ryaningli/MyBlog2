from rest_framework import exceptions
from django.http import Http404
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import set_rollback
from Application.utils import custom_exceptions


def custom_exception_handler(exc, context):
    """
    Returns the response that should be used for any given exception.

    By default we handle the REST framework `APIException`, and also
    Django's built-in `Http404` and `PermissionDenied` exceptions.

    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.

    自定义异常处理，当exc为自定义的异常类时，也加入Response返回
    isinstance(exc, custom_exceptions.APIException)
    """
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, custom_exceptions.APIException) or isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        # if isinstance(exc.detail, (list, dict)):
        #     data = exc.detail
        # else:
        #     data = {'detail': exc.detail}
        data = {}
        if isinstance(exc, exceptions.APIException):
            if isinstance(exc.detail, (list, dict)):
                data['code'] = exc.status_code
                data['result'] = False
                data['msg'] = '请求异常'
                data['data'] = exc.detail
            else:
                data['code'] = exc.status_code
                data['result'] = False
                data['msg'] = exc.detail
                data['data'] = {}
        else:
            data = exc.detail

        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)

    return None
