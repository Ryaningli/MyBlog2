from collections import OrderedDict
from rest_framework.response import Response as Rp
from rest_framework import status

from Blog.utils.ERROR_CODE import ERROR_CODE

BASE_ERROR_CREATED = ['unique']
BASE_ERROR_BAD_DATA = ['max_length', 'min_length']


class Response(Rp):
    def __init__(self, serializer=None, code=0, result=True, data=None, msg=None, state=None, template_name=None,
                 headers=None, exception=False, content_type=None):
        self.code = code
        self.result = result
        self.data = data
        self.msg = msg

        self.json_data = {
            'code': code,
            'result': result,
            'data': data,
            'msg': msg
        }

        if serializer is not None:
            em_order = list(OrderedDict(serializer.errors).items())[0]
            em = (em_order[0], em_order[1][0])
            if em[1].code in BASE_ERROR_CREATED:
                self.json_data = self.set_json_data(error_name='CREATED', serializer=serializer, code=code, result=result, data=data, msg=msg)
            elif em[1].code in BASE_ERROR_BAD_DATA:
                self.json_data = self.set_json_data(error_name='BAD_DATA', serializer=serializer, code=code, result=result, data=data, msg=msg)

        super(Response, self).__init__(data=self.json_data, status=state, template_name=template_name, headers=headers,
                                       exception=exception, content_type=content_type)

    @staticmethod
    def set_json_data(error_name=None, serializer=None, code=0, result=True, data=None, msg=None):
        ser_msg = None
        if serializer:
            em_order = list(OrderedDict(serializer.errors).items())[0]
            em = (em_order[0], em_order[1][0])
            ser_msg = (serializer[em[0]].label or em[0]) + ': ' + em[1] if serializer[em[0]].label not in em[1]\
                else serializer.errors[em[0]][0]

        msg = msg or ser_msg

        if error_name:
            j = ERROR_CODE[error_name]
            json_data = {
                'code': code or j['code'],
                'result': result or j['result'],
                'data': data or j['data'],
                'msg': msg or j['msg']
            }
            return json_data
        else:
            return {
                'code': code,
                'result': result,
                'data': data,
                'msg': msg
            }

    def get_rp(self, code=0, result=True, data=None, msg=None, state=None):
        data = {
            'code': code,
            'result': result,
            'data': data,
            'msg': msg
        }
        return Rp(data=data, status=state, template_name=self.template_name, headers=self.headers,
                  exception=self.exception, content_type=self.content_type)

    @property
    def SUCCESS(self):
        return self.get_rp(code=self.code or 0, result=True, data=self.data, msg=self.msg or '处理成功')

    @property
    def BAD_DATA(self):
        return self.get_rp(code=self.code or 20001, result=False, data=self.data, msg=self.msg or '参数错误')

    @property
    def CREATED(self):
        return self.get_rp(code=self.code or 40001, result=False, data=self.data, msg=self.msg or '已存在',
                           state=status.HTTP_201_CREATED)
