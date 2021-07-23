def ResponseData(code=None, result=None, msg=None, data=None, **kwargs):
    if code is None:
        code = 0
    if result is None:
        result = True
    if msg is None:
        msg = '请求成功'
    if data is None:
        data = {}
    response = {
        'code': code,
        'result': result,
        'msg': msg,
        'data': data
    }

    if isinstance(response['data'], dict):
        response['data'].update(**kwargs)

    return response
