class Pra():
    def __new__(cls, *args, **kwargs):
        return '父类'


class Son(Pra):
    def __init__(self):
        super(Son, self).__init__()
    
    def son_m(self):
        return '子类方法'


print(Son().son_m())