from PPTwoPlayerGame import PPTwoPlayerGame #TODO may also need to import the error.

'''
PPWithNNTwoPlayerGame is an abstract class
...for any two player game where the game has a state
...and players can make moves (represented by numbers or strings).
If all of the methods are implemented, a PPWithNNPlayer (Policy Player With Neural Network Player) can learn to play the game.
'''

#TODO need to figure out if inputLen are class properties or otherwise
class PPWithNNTwoPlayerGame(PPTwoPlayerGame):
    #a list of all the possible moves that can ever be done in the game no matter the situation
    #this is needed because the neural net always needs to have all options available in order to generalize/learn
    #self.getPossibleMoves() (defined in the super class) may only return a list of elements contained in this list
    allMoves = []
    #length of the list returned by strToNNInput
    inputLen = 0 #len(PPWithNNTwoPlayerGame().strToNNInput())
    #length of allMoves
    outputLen = 0 #len(allMoves)
    
    def __init__(self):
        PPTwoPlayerGame.__init__(self)
        
    #Needed in order to have a NeuralNet learn from a PolicyPlayer
    #Converts the string returned by convertToStr into a unique list with a constant length
    #By constant length, I mean that the length of the list returned by this function
    #must always be the same, regardless of the input.
    def strToNNInput(self, string):
        raise NotImplementedError
        
    