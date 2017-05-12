'''
The goal is to have a class where if anything subclasses it, they are forced to have certain class attributes.
Normal instance properties work just fine like this because of the whole "init" thing.

'''


class Meta1(type):
    def __new__(mcls, name, bases, namespace):
        print("using Meta1")
        cls = super().__new__(mcls, name, bases, namespace)
        return cls

class Meta2(type):
    def __new__(mcls, name, bases, namespace):
        print("using Meta2")
        cls = super().__new__(mcls, name, bases, namespace)
        return cls
        
class SubMeta1(Meta1):
    def __new__(mcls, name, bases, namespace):
        print("using SubMeta1")
        print("metaclass name: {}".format(mcls.__name__))
        cls = type.__new__(mcls, name, bases, namespace)
        return cls

class MetaMeta1(metaclass=Meta1):
    pass

class MetaMeta2(metaclass=Meta2):
    pass

print("about to test")

class MetaAndSubOfMeta1(Meta1, metaclass=Meta1):
    pass

a = MetaAndSubOfMeta1()
print(type(a))
print(a.__)
'''
class MetaSubMeta1(metaclass=SubMeta1):
    pass


class SubMetaMeta1AndSubMetaMeta2(MetaMeta1, MetaMeta2):
    pass
    
'''