from rest_framework.renderers import JSONRenderer


class CustomRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        :param data: 返回的数据
        :param accepted_media_type: 接收的类型
        :param renderer_context:  渲染呈现的内容
        """
        # 如果有请求数据过来：类似之前的if request.method == "POST"
        if renderer_context:
            # 判断返回的数据是否为字典
            if isinstance(data, dict) and all(map(lambda x: x in data, ['code', 'result', 'msg', 'data'])):
                code = data.pop('code', 0)
                result = data.pop('result', True)
                msg = data.pop('msg', '请求成功')
                rp_data = data.pop('data', {})
            else:
                code = 0
                result = True
                msg = '请求成功'
                rp_data = data

            # 重新构建返回数据的格式
            ret = {
                'code': code,
                'result': result,
                'msg': msg,
                'data': rp_data
            }
            # 根据父类方式返回数据格式
            return super().render(ret, accepted_media_type, renderer_context)
        else:  # 如果没有发生修改则返回原格式数据
            return super().render(data, accepted_media_type, renderer_context)