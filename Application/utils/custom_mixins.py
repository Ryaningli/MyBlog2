from rest_framework.mixins import DestroyModelMixin


class FakeDestroyModelMixin(DestroyModelMixin):
    """
    虚假删除
    """
    def perform_destroy(self, instance):
        instance.state = 0
        instance.save()
