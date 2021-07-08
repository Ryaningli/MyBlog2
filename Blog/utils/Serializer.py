from collections import OrderedDict
from rest_framework import serializers
from Blog.utils.ERROR_CODE import CODE_BIND, ERROR_CODE


def get_response_data(serializer, code=0, result=False, data=None, msg=None):
    if serializer.is_valid():
        return {
            'code': code,
            'result': True,
            'data': data or serializer.data,
            'msg': msg or '处理成功'
        }

    em_order = list(OrderedDict(serializer.errors).items())[0]
    em = (em_order[0], em_order[1][0])

    err_code = em[1].code
    err_msg = (serializer[em[0]].label or em[0]) + ': ' + em[1] if serializer[em[0]].label not in em[1] \
        else serializer.errors[em[0]][0]

    response_data = {}
    for key in CODE_BIND:
        if err_code in CODE_BIND[key]:
            response_data = ERROR_CODE[key]
            break

    if not response_data:
        response_data = ERROR_CODE['BAD_DATA']

    response_data['code'] = code or response_data['code']
    response_data['result'] = result or response_data['result']
    response_data['data'] = data or response_data['data'] or serializer.errors
    response_data['msg'] = msg or err_msg or response_data['msg']

    return response_data


class Serializer(serializers.Serializer):
    """
    重写serializers.Serializer，添加只读方法error，组合返回msg
    """
    def __init__(self, *args, **kwargs):
        super(Serializer, self).__init__(*args, **kwargs)

    @property
    def response(self):
        return get_response_data(self)


class ModelSerializer(serializers.ModelSerializer):
    """
    重写serializers.Serializer，添加只读方法error，组合返回msg
    """
    def __init__(self, *args, **kwargs):
        super(ModelSerializer, self).__init__(*args, **kwargs)

    def response(self, code=0, result=False, data=None, msg=None):
        return get_response_data(self, code=code, result=result, data=data, msg=msg)


