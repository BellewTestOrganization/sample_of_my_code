

def singleton(cls):
    singleton_instances = {}

    def get(*args, **kwargs):
        if not singleton_instances.get(cls):
            singleton_instances[cls] = cls(*args, **kwargs)
        return singleton_instances[cls]

    return get


@singleton
class TestSingletonClass(object):

    def __init__(self):
        print('init')

a = TestSingletonClass()
b = TestSingletonClass()
