'''
I want to be able to subclass a class, and have the subclass fail to be created unless it has some attributes

In my ideal world, I would have each one of these attributes have a decorator.
Can you use a decorator on a variable? No.

So then the next best way to do it is for each subclass to be forced to have a property called
requiredAttributes and then each subclass of each of those is required to have those attributes.

This may fail when subclassing from multiple classes if the metaclass doesn't enforce it.
Let's see, that metaclass would have to be a subclass of all the other metaclasses
So another metaclass could override it, but it would have to do so on-purpose, in which case they would know.

So in order to make sure you're actually trying to use the functionailty, we need to make sure
1. I am your metaclass and
2. I'm not just your metaclass because you're subclassing something that has me as the metaclass

(1) is taken care of because __new__ is never called unless I'm your metaclass
for (2), we go through each subclass and make sure I'm not the metaclass

The current version I have fails if you want to have your own required attributes and subclass something that requires you to have attributes.
Actually, I'm wrong.
Currently, the metaclass doesn't care if you have your own required attributes or not.
It's only checked when something tries to subclass you. So if you do have your own, they will be required.

So will it/should it require all the attributes all the way down the inheritance tree?
Let's see what ABCMeta does.

Oh, just like ABCMeta, it doesn't matter. If a parent class already implements them, and you're subclassing, you'll just get them from it.
'''
from abc import ABCMeta

class NoRequirements(RuntimeError):
        def __init__(self, message):
            RuntimeError.__init__(self, message)

class ABCAMeta(ABCMeta):
    def __init__(mcls, name, bases, namespace):
        ABCMeta.__init__(mcls, name, bases, namespace)

    def __new__(mcls, name, bases, namespace):
        def getRequirements(c):
            """c is a class that should have a 'requiredAttributes' attribute
            this function will get that list of required attributes or
            raise a NoRequirements error if it doesn't find one.
            """

            if hasattr(c, 'requiredAttributes'):
                return c.requiredAttributes
            else:
                raise NoRequirements("Class {} has no requiredAttributes property".format(c.__name__))

        cls = super().__new__(mcls, name, bases, namespace)
        #true if no parents of the class being created have ABCAMeta as their metaclass
        basicMetaclass = True 
        #list of attributes the class being created must implement
        #should stay empty if basicMetaclass stays True
        reqs = [] 
        for parent in bases:
            parentMeta = type(parent)
            if parentMeta==ABCAMeta:
                #the class being created has a parent whose metaclass is ABCAMeta
                #the class being created must contain the requirements of the parent class
                basicMetaclass=False
                try:
                    reqs.extend(getRequirements(parent))
                except NoRequirements:
                    raise
        #will force subclasses of the created class to define
        #the atrributes listed in the requiredAttributes attribute of the created class
        if basicMetaclass:
            getRequirements(cls) #just want it to raise an error if it doesn't have the attributes
        else:
            missingreqs = []
            for req in reqs:
                if not hasattr(cls, req):
                    missingreqs.append(req)
            if len(missingreqs)!=0:
                raise NameError("Class {} has not implemented the following attributes: {}".format(cls.__name__, str(missingreqs)[1:-1]))
        return cls

class AbstractFoo(metaclass=ABCAMeta):
    requiredAttributes = ['forceThis']

class RealFoo(AbstractFoo):
    pass


'''
class metata(type):
    pass

class yo(metaclass=ABCMeta):
    @abstractmethod
    def hello():
        pass

class jo(yo):
    pass
'''


'''
class ForceMeta(type):
    required = ['foo', 'bar']

    def __new__(mcls, name, bases, namespace):
        print("using new!")
        print("mcls: {}".format(mcls))
        print(ForceMeta)
        cls = super().__new__(mcls, name, bases, namespace)
        for prop in mcls.required:
            if not hasattr(cls, prop):
               raise NotImplementedError('must define {}'.format(prop))
        for base in bases:
            print(base)
        return cls

class BelowForceMeta(metaclass=ForceMeta):
    foo = 1
    bar = 2

class BBFM(BelowForceMeta):
    pass

class MyForceMeta(type):
    def __init__(self, requiredAttributes):
        self.requiredAttributes = requiredAttributes
        
    def __new__(mcls, name, bases, namespace):
        cls = super().__new__(mcls, name, bases, namespace)
        for prop in mcls.required:
            if not hasattr(cls, prop):
               raise NotImplementedError('must define {}'.format(prop))
        return cls
        
a = BBFM()
'''