class B(type):
    def __new__(cls, *args, **kwargs):
        print('wdawdad')


class A(metaclass=B):
    pass

a = A()
