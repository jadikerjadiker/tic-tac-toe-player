class Superclass:
    def makeNew(self):
        return self.__class__()

class Subclass(Superclass):
    #DONT DO THIS
    '''
    def __init__(self, value = [1]):
        self.value = value
    '''
    
    #Do this
    def __init__(self, value = None):
        if value is None:
            self.value = [1]
        
    def setValue(self, newValue):
        self.value[0] = newValue
        
if __name__ == "__main__":
    s = Subclass()
    s.setValue(5)
    other = s.makeNew()
    print(s.value)
    print(other.value)