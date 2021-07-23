from rest_framework import serializers


class StandardDateTimeField(serializers.DateTimeField):
    def __init__(self, format='%Y-%m-%d %H:%M:%S', input_formats=None, default_timezone=None, *args, **kwargs):
        super(StandardDateTimeField, self).__init__(format, input_formats, default_timezone, *args, **kwargs)