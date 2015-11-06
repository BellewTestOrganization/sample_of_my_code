
class Singleton:
    cls = None
    instance = None

    def __init__(self, cls):
        self.cls = cls
        self.instance = None

    def __call__(self, *args, **kwds):
        if self.instance is None:
            self.instance = self.cls(*args, **kwds)
        return self.instance


@Singleton
class TestSingletonClass(object):

    def __init__(self):
        print('init')
        
a = TestSingletonClass()
b = TestSingletonClass()
