from collections import OrderedDict
from rest_framework import status as stat
from rest_framework.permissions import BasePermission


class APIException(Exception):
    """
    Base class for REST framework exceptions.
    Subclasses should provide `.status_code` and `.default_detail` properties.
    """
    status_code = stat.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = {}
    default_code = 20001
    default_result = False
    default_msg = '未定义错误'
    default_data = {}

    def __init__(self, msg=None, serializer=None, code=None, result=None, data=None, status=None, **kwargs):
        print(serializer)
        if serializer is not None:
            if not serializer.is_valid():
                em_order = list(OrderedDict(serializer.errors).items())[0]
                field, error = em_order[0], em_order[1][0]
                try:
                    ser_msg = (serializer[field].label or field) + ': ' + error \
                        if serializer[field].label not in error else error
                except KeyError:
                    ser_msg = error
            else:
                ser_msg = '序列化验证有效'
        else:
            ser_msg = None

        if code is None:
            code = self.default_code
        if result is None:
            result = self.default_result
        if msg is None:
            msg = ser_msg or self.default_msg
        if data is None:
            data = self.default_data
        if status is not None:
            self.status_code = status

        self.detail = {
            'code': code,
            'result': result,
            'msg': msg,
            'data': data
        }

        self.detail['data'].update(**kwargs)
        # self.detail = _get_error_details(detail, code)  # 去掉这一步，防止json数据全部被格式化成字符串


class AuthenticationFailed(APIException):
    status_code = stat.HTTP_401_UNAUTHORIZED
    default_code = 4200
    default_msg = '鉴权失败'


class Forbidden(APIException):
    status_code = stat.HTTP_403_FORBIDDEN
    default_code = 4100
    default_msg = '您没有执行该操作的权限'


class BadParameter(APIException):
    status_code = stat.HTTP_400_BAD_REQUEST
    default_code = 401
    default_msg = '参数错误'


class IsAdminUser(BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        if bool(request.user and request.user.is_staff):
            return True
        else:
            raise Forbidden


if __name__ == '__main__':
    IsAdminUser()