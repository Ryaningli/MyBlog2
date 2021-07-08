ERROR_CODE = {
    'SUCCESS': {'code': 0, 'result': True, 'data': None, 'msg': '处理成功'},
    'BAD_DATA': {'code': 20001, 'result': False, 'data': None, 'msg': '参数有误'},
    'CREATED': {'code': 40001, 'result': False, 'data': None, 'msg': '已存在'},
}

CODE_BIND = {
    'SUCCESS': [],
    'BAD_DATA': [],
    'CREATED': ['unique']
}