from functools import reduce

res = {
    'code': 0,
    'result': True,
    'msg': 'dasd',
    'data': {}
}
li = ['code', 'result', ]

res1 = {
    'code': 0,
    'result': True,
    'msg': 'dasd',
    'data': {}
}

a = reduce(lambda x, y: x and y, map(lambda z: z in res, li))

print(a)