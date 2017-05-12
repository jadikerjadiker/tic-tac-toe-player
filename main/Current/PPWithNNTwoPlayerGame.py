from PPTwoPlayerGame import PPTwoPlayerGame #TODO may also need to import the error.
from UsefulThings import assertPython3
from abc import abstractmethod
from abca import ABCAMeta
assertPython3()

'''
PPWithNNTwoPlayerGame is an abstract class
...for any two player game where the game has a state
...and players can make moves (represented by numbers or strings).
If all of the methods are implemented, a PPWithNNPlayer (Policy Player With Neural Network Player) can learn to play the game.
'''

#TODO need to figure out if inputLen are class properties or otherwise
class PPWithNNTwoPlayerGame(PPTwoPlayerGame, metaclass=ABCAMeta):
    requiredAttributes = []
    
    #length of the list returned by strToNNInput
    #len(PPWithNNTwoPlayerGame().strToNNInput())
    requiredAttributes.append("inputLen")
    
    #length of allMoves
    #len(allMoves)
    requiredAttributes.append("outputLen") 
    
    @classmethod
    @abstractmethod
    def allMoves(self):
        """a list of all the possible moves that can ever be done in the game no matter the situation
        this is needed because the neural net always needs to have all options available in order to generalize/learn
        self.getPossibleMoves() (defined in the super class) may only return a list of elements contained in this list
        """
    
    
    @classmethod #this must go before the abstractmethod
    @abstractmethod
    def strToNNInput(self, string):
        """Converts the string returned by convertToStr into a neural network input
        Returns a list with a consistent length that only contains numbers
        Consistent length means that the length of the list is always the same, regardless of the input.
        """
    
    def __init__(self):
        PPTwoPlayerGame.__init__(self)
        
    
if __name__ == "__main__":
    class EZ(PPWithNNTwoPlayerGame):
        def __init__(self):
            PPWithNNTwoPlayerGame.__init__(self)
            
        #@classmethod
        #def strToNNInput(self, string):
        #    return [string]
        
        @classmethod
        def allMoves(self):
            pass
        
    a = EZ()
    print(EZ.allMoves)
    print(EZ.strToNNInput("hi"))
    #a.allMoves = [1, 2, 3]
    #print(a.allMoves)

    