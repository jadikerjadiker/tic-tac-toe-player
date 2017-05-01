from PPTwoPlayerGame import PPTwoPlayerGame #TODO may also need to import the error.

'''
PPWithNNTwoPlayerGame is an abstract class
...for any two player game where the game has a state
...and players can make moves (represented by numbers or strings).
If all of the methods are implemented, a PPWithNNPlayer (Policy Player With Neural Network Player) can learn to play the game.
'''

class PPWithNNTwoPlayerGame(PPTwoPlayerGame):
    def __init__(self, allMoves):
        PPTwoPlayerGame.__init__(self)
        #a list of all the possible moves that can ever be done in the game no matter the situation
        #this is needed because the neural net always needs to have all options available in order to generalize/learn
        #self.getPossibleMoves() (defined in the super class) may only return a list of elements contained in this list
        self.allMoves = allMoves
        
        self.inputLen = None
        self.outputLen = None
        self.setInputLen()
        self.setOutputLen()
    
    #return the length of the list returned by self.strToNNInput   
    def setInputLen(self):
        #This is a really expensive implementation.
        #Really you should just be returning a number
        return len(self.strToNNInput(self.convertToStr()))
    
    #return the length of self.allMoves
    #In other words, return how many different possible actions there are in this game,
    #which will be the length of the output of the neural network
    def setOutputLen(self):
        #This is a really expensive implementation.
        #Really you should just be returning a number
        return len(self.allMoves)
        
    #Needed in order to have a NeuralNet learn from a PolicyPlayer
    #Converts the string returned by convertToStr into a unique list with a constant length
    #By constant length, I mean that the length of the list returned by this function
    #must always be the same, regardless of the input.
    def strToNNInput(self, string):
        raise NotImplementedError
        
    