class A:
    def a(self):
        print('aaaaa')

class B(A):
    def a(self):
        print('bbbbbbbb')
        super(B, self).a()

B().a()