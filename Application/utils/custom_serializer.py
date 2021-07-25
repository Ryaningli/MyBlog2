from rest_framework.exceptions import ValidationError
from rest_framework.serializers import BaseSerializer, SerializerMetaclass, Serializer as Ser, ModelSerializer as Mod
from django.db import models
from Application.utils.custom_exceptions import BadRequest
from Application.utils.custom_serializer_fields import StandardDateTimeField


class CustomBaseSerializer(BaseSerializer):
    """
    默认抛起错误
    自动组合错误信息
    """

    def is_valid(self, raise_exception=True):
        assert hasattr(self, 'initial_data'), (
            'Cannot call `.is_valid()` as no `data=` keyword argument was '
            'passed when instantiating the serializer instance.'
        )

        if not hasattr(self, '_validated_data'):
            try:
                self._validated_data = self.run_validation(self.initial_data)
            except ValidationError as exc:
                self._validated_data = {}
                self._errors = exc.detail
            else:
                self._errors = {}

        if self._errors and raise_exception:
            raise BadRequest(serializer=self)

        return not bool(self._errors)


class Serializer(CustomBaseSerializer, Ser, metaclass=SerializerMetaclass):
    ...


class ModelSerializer(CustomBaseSerializer, Mod, metaclass=SerializerMetaclass):
    serializer_field_mapping = Mod.serializer_field_mapping
    serializer_field_mapping[models.DateTimeField] = StandardDateTimeField      # 将数据库的datetime字段默认格式化为标准时间显示
