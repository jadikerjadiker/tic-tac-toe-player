from PPTwoPlayerGame import PPTwoPlayerGame #TODO may also need to import the error.

'''
PPWithNNTwoPlayerGame is an abstract class (with the occasional pre-implemented method)
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
        
        
    #Needed in order to have a NeuralNet learn from a PolicyPlayer
    #Converts the string returned by convertToStr into a unique list with a constant length
    #By constant length, I mean that the length of the list returned by this function
    #must always be the same, regardless of the input.
    def strToConstLenList(self, string):
        raise NotImplementedError
        
        
    