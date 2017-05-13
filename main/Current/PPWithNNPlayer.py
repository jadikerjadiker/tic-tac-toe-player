from PolicyPlayer import PolicyPlayer
from TwoPlayerGamePlayer import TwoPlayerGamePlayer
from NeuralNet import NeuralNet
from overrides import overrides

#TODO del import
from UsefulThings import printAndReturn

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

class PPWithNNPlayer(TwoPlayerGamePlayer):
    #policyPlayerInfo and neuralNetInfo are both dictionaries
    #which contain all the paramters (including positional) for their respective class inits
    #The only difference is that neuralNetInfo's "architecture" parameter should not include an input or output layer
    #those layers in the architecture (which are dependant on the game) will be automatically added in this init.
    def __init__(self, gameClass, policyPlayerInfo = {}, neuralNetInfo = {}):
        self.gameClass = gameClass
        #the architecture of the neural net; how many neurons are in each layer
        architecture = [gameClass.inputLen] #first layer (input) must be the correct amount for the game
        try:
            architecture.extend(neuralNetInfo.pop("architecture"))
        except KeyError: #no architecture specified
            raise RuntimeError("Need to specify an (internal neural net) architecture when creating PPWithNNPlayer")
        architecture.append(gameClass.outputLen) #last layer (output) must be the correct amount for the game
        
        for reward in policyPlayerInfo.get("rewards", []):
            #The neural net can't output anything outside of the range 0 inclusive to 1 inclusive.
            #So if any of the rewards are out of this range, that will cause an issue.
            #If none of the rewards are out of this range, it won't be an issue because the policy player doesn't accumulate rewards.
            self.checkReward(reward)
        self.policyPlayer = PolicyPlayer(**policyPlayerInfo)
        self.neuralNet = NeuralNet(architecture, **neuralNetInfo)
        
        #if @training is True, then makeMove will cause the policy player to train on the data
        #if @training is False, then makeMove will have the neural net predict make the move
        self.training = True
    
    def checkReward(self, reward):
        if reward>1 or reward<0:
                raise ValueError("Reward of {} is not in between 0 and 1".format(reward))
     
    @overrides
    def makeMove(self, *args, **kwargs):
        if self.training:
            self.policyPlayer.makeMove(*args, **kwargs)
        else:
            #TODO have the neural net make a move
            self.policyPlayer.exploreRate = 0
            self.policyPlayer.makeMove(*args, **kwargs)
    
    @overrides
    def update(self, *args, **kwargs):
        if self.training: #learning how to play the game
            self.policyPlayer.update(*args, **kwargs)
        else: #generalizing what I've learned
            #the next bit of code converts the policy player into a dataset
            '''
            TODO delete thinking
            
            Each of the policies of the player needs to become one training example.
            Need to find some way to loop through all of the training examples.
            For now, it will all be one huge batch.
            So the final result will be [dataset] where
            dataset = [(input, output), ...]
            
            Looks like the PolicyPlayer has a property called policies that we can just iterate through.
            use policies.items from
            http://stackoverflow.com/questions/674519/how-can-i-convert-a-python-dictionary-to-a-list-of-tuples
            to turn it into a list of tuples
            Then, for each one of those tuples, convert it into the lists you want.
            Something like
            [(convertPPKeyToNN(key), convertPPValueToNN(value)) for (key, value) in policies.items]
            Then, that becomes the dataset
            '''
            #the key is the string representing a game position
            def convertPPToNNInput(key):
                #returns a constant-lengthed list of numbers
                return gameClass.strToNNInput(key)
            
            #convert a Policy into a target for a NeuralNet
            #defaultReward is the target output used for actions
            #that are not available to the player in the given situation.
            def convertPPToNNOutput(defaultReward, policy):
                #assume no actions are possible
                ans = [defaultReward]*len(self.gameClass.allMoves)
                
                #for each action that is possible, update its value
                for action in policy.getAllActions():
                    index = self.gameClass.allMoves.index(action) #find the index for ans
                    ans[index] = policy.getValueForAction(action) #set the value to be what the policy player determined
                    
                return ans

            #The reward for trying to make a move that can't be made
            defaultReward = kwargs.get("defaultReward", 0)
            self.checkReward(defaultReward)
            batch = [(printAndReturn(convertPPToNNInput(gameString)), printAndReturn(convertPPToNNOutput(defaultReward, policy))) for (gameString, policy) in self.policyPlayer.policies.items()]
            dataset = [batch]
            print("dataset")
            print(dataset)
            
            print("architecture")
            print(self.neuralNet.architecture)
            #**kwargs is passed to neural net for training parameters
            self.neuralNet.train(dataset, **kwargs)
        

if __name__ == "__main__":
    from TwoPlayerGameRunner import TwoPlayerGameRunner
    from ChopsticksGame import ChopsticksGame
    import UsefulThings as useful
    import Testers as test
    from ChopsticksOverAndOutGame import ChopsticksOverAndOutGame
    from TicTacToeGame import TicTacToeGame
    
    #TODO finish
    
    policyPlayerInfo = {"exploreRate":0, "learningRate":.5, "rewards":[0, .5, 1], "defaultPolicyValue":.2}
    neuralNetInfo = {"architecture":[9, 9], "learningRate":.01}
    neuralNetTrainingInfo = {"mode":("avg", .1), "comment":2}
    
    gameClass = TicTacToeGame
    gameRunner = TwoPlayerGameRunner(gameClass)
    gamesToPlay = 100
    p = PPWithNNPlayer(gameClass, policyPlayerInfo, neuralNetInfo)
    #p.load("saved.pkl")
    for i in range(gamesToPlay):
        useful.printPercent(i, gamesToPlay, 5, 1)
        g = gameRunner.play(who = (p, 'random'))
        p.update()
    
    p.training = False
    #learningRate = None, mode = None, trainAway = False, comment = False
    print("About to update")
    p.update(**neuralNetTrainingInfo)
    '''
    test.testAgainstRandom(p, gameClass, )
    #p.save("saved.pkl")
    while True:
        gameRunner.play(who = (p, "human"))
    '''