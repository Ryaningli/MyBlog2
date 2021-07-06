class ResponseData:
    def __init__(self, code=0, result=True, data=None, msg=None):
        self.code = code
        self.result = result
        self.data = data
        self.msg = msg
        self.SUCCESS = self.get_data(code=code or 0, result=result, data=data, msg=msg or '处理成功')
        self.BAD_REQUEST_PARAMETER = self.get_data(code=400, result=False, data=data, msg=msg)

    @staticmethod
    def get_data(code=0, result=True, data=None, msg=None):
        return {
            'code': code,
            'result': result,
            'data': data,
            'msg': msg
        }
