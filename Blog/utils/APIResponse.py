from collections import OrderedDict
from rest_framework.response import Response


def get_data_by_order(*args):
    """
    :param args:
    :return: 根据传参的顺序，返回非None的第一个
    """
    result = None
    for arg in args:
        if arg is not None:
            result = arg
            break
    return result


class APIResponse(Response):
    """
    继承Response
    优先取传参，其次取模板， 再其次取序列化错误数据
    """
    def __init__(self, serializer=None, code=None, result=None, msg=None, data=None, template=None, status=None,
                 headers=None, exception=False, content_type=None, **kwargs):
        if serializer is not None:
            if not serializer.is_valid():
                em_order = list(OrderedDict(serializer.errors).items())[0]
                field, error = em_order[0], em_order[1][0]
                ser_code = 20001
                ser_result = False
                try:
                    ser_msg = (serializer[field].label or field) + ': ' + error \
                        if serializer[field].label not in error else error
                except KeyError:
                    ser_msg = error

                # 将序列化器的错误信息添加至data
                # ser_data = serializer.errors
                ser_data = None
            else:
                ser_code = 0
                ser_result = True
                ser_msg = '处理成功'
                ser_data = serializer.data
        else:
            ser_code = None
            ser_result = None
            ser_msg = None
            ser_data = None

        if template is not None:
            tem_code = template['code']
            tem_result = template['result']
            tem_msg = template['msg']
            tem_data = template['data']
        else:
            tem_code = None
            tem_result = None
            tem_msg = None
            tem_data = None

        response_json = {
            'code': get_data_by_order(code, tem_code, ser_code, 0),
            'result': get_data_by_order(result, tem_result, ser_result, True),
            'msg': get_data_by_order(msg, tem_msg, ser_msg, '处理成功'),
            'data': get_data_by_order(data, tem_data, ser_data, {})
        }

        response_json['data'].update(**kwargs)

        super(APIResponse, self).__init__(data=response_json, status=status, headers=headers, exception=exception,
                                          content_type=content_type)


def get_json(code, result, msg, data=None):
    data = {
        'code': code,
        'result': result,
        'msg': msg,
        'data': data
    }
    return data


class ResponseTemplate:
    SUCCESS = get_json(code=0, result=True, msg='处理成功')
    BAD_DATA = get_json(code=20001, result=False, msg='参数错误')
    FORBIDDEN = get_json(code=40003, result=False, msg='用户名或密码错误')
