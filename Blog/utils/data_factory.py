from rest_framework.response import Response as Rp
from rest_framework import status


class Response(Rp):
    def __init__(self, code=0, result=True, data=None, msg=None, status=None, template_name=None, headers=None,
                 exception=False, content_type=None):
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
        super(Response, self).__init__(data=self.json_data, status=status, template_name=template_name, headers=headers,
                                       exception=exception, content_type=content_type)

    def get_rp(self, code=0, result=True, data=None, msg=None, status=None):
        data = {
            'code': code,
            'result': result,
            'data': data,
            'msg': msg
        }
        return Rp(data=data, status=status, template_name=self.template_name, headers=self.headers,
                  exception=self.exception, content_type=self.content_type)

    @property
    def SUCCESS(self):
        return self.get_rp(code=self.code or 0, result=True, data=self.data, msg=self.msg or '处理成功')

    @property
    def BAD_PARAMETER(self):
        return self.get_rp(code=self.code or 20001, result=False, data=self.data, msg=self.msg or '参数错误')

    @property
    def CREATED(self):
        return self.get_rp(code=self.code or 40001, result=False, data=self.data, msg=self.msg or '已存在')
