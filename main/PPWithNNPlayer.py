from PolicyPlayer import PolicyPlayer
from NeuralNet import NeuralNet

'''
The goal of this class is to have a computer that uses reinforcement learning in
...order to understand best strategies to win the game, and uses
...a neural network to generalize those strategies
...so the policy player does not have to play as many games in order to do well.

The main difference between this player and a TwoPlayerPolicyPlayer
...is that this player will use a neural net to both make and update its decisions.

This class has two parts: the policyPlayer and the neuralNet
The policy player trains on the game for a certain amount of time.
Then, all the data from the policy player is turned into a dataset for the neural net to learn from.

'''

class PPWithNNPlayer():
    #policyPlayerInfo and neuralNetInfo are both dictionaries
    #which contain all the paramters (including positional) for their respective class inits
    #The only difference is that neuralNetInfo's "architecture" parameter should not include an input or output layer
    #those layers in the architecture (which are dependant on the game) will be automatically added in this init.
    def __init__(self, game, policyPlayerInfo = {}, neuralNetInfo = {}):
        self.game = game
        #the architecture of the neural net; how many neurons are in each layer
        architecture = [game.inputLen] #first layer (input) must be the correct amount for the game
        try:
            architecture.extend(neuralNetInfo.pop("architecture"))
        except KeyError: #no architecture specified
            raise RuntimeError("Need to specify an internal neural net architecture when creating PPWithNNPlayer")
        architecture.append(game.outputLen) #last layer (output) must be the correct amount for the game
            
        self.policyPlayer = PolicyPlayer(**policyPlayerInfo)
        self.neuralNet = NeuralNet(architecture, **neuralNetInfo)
        

if __name__ == "__main__":
    print("hi")