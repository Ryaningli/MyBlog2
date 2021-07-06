from rest_framework import serializers


class Serializer(serializers.Serializer):
    """
    重写serializers.Serializer，添加只读方法error，组合返回msg
    """
    def __init__(self, *args, **kwargs):
        super(Serializer, self).__init__(*args, **kwargs)

    @property
    def error(self):
        for field in self.errors:
            return (self[field].label or field) + ': ' + self.errors[field][0]
        return None


class ModelSerializer(serializers.ModelSerializer):
    """
    重写serializers.Serializer，添加只读方法error，组合返回msg
    """
    def __init__(self, *args, **kwargs):
        super(ModelSerializer, self).__init__(*args, **kwargs)

    @property
    def error(self):
        for field in self.errors:
            if self[field].label in self.errors[field][0]:  # 如果字段名存在与错误信息中，则不用组合
                return self.errors[field][0]
            return (self[field].label or field) + ': ' + self.errors[field][0]
            # return '【{}】{}'.format(self[field].label or field, self.errors[field][0])
        return None


