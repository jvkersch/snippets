class Meta(type):

    def __new__(cls, class_name, bases, class_dict):
        print(class_name)
        print(bases)
        print(class_dict)
        return type.__new__(cls, class_name, bases, class_dict)


class A(object):

    __metaclass__ = Meta

    a = 34

    
