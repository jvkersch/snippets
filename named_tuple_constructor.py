""" namedtuple example.

namedtuple calls __new__ instead of __init__ during construction.

"""

from collections import namedtuple


A = namedtuple('A', ['value'])


class B(A):

    def __init__(self, value):
        value = unicode(value, 'utf-8')
        super(B, self).__init__(value)

    def __new__(cls, *args):
        print 'Peeakaboo', cls, args
        return super(B, cls).__new__(cls, *args)


if __name__ == '__main__':
    b = B("this should become unicode")
    print type(b.value)
    print b
