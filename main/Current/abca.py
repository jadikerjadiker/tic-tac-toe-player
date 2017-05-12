from abc import ABCMeta

class NoRequirements(RuntimeError):
        def __init__(self, message):
            RuntimeError.__init__(self, message)

class ABCAMeta(ABCMeta):
    """ABCAMeta (the last 'A' stands for 'Attributes').

    The class has two ways of working.

    1. A class which just uses ABCAMeta as a metaclass must have a property called requiredAttributes
    ...which should contain a list of the names of all the attributes you want to require on future subclasses of that class
    
    2. A class whose parent's metaclass is ABCAMeta must have all the required attributes specified by that parent class.
    
    For example, the following code,

    class AbstractFoo(metaclass=ABCAMeta):
        requiredAttributes = ['forceThis']
    
    class RealFoo(AbstractFoo):
        pass
        
    will throw an error:
    NameError: Class RealFoo has not implemented the following attributes: 'forceThis'
    """
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
                raise NameError("Class {} has not implemented the following attributes: {}".format(
                    cls.__name__, (str(missingreqs)[1:-1]).replace("'", "")))
        return cls