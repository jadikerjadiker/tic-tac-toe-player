from abc import ABCMeta, abstractmethod

class A(metaclass=ABCMeta):
    @abstractmethod
    def hi(self):
        pass
    
class B(A):
    def hi(self):
        pass
    
class C(B):
    pass