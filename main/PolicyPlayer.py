import random
import sys
import UsefulThings as useful

assert sys.version_info[0] >= 3, "Python version needs to be at least 3"
'''
Policy Player

Creates a policy for each position on the board.

A policy consists of a list of 9 values, each representing a probability...
of winning if you take that spot

A complete policy would hold 1329 different board positions:
(9*7*5*3*1) = 945 for going first, and 2*4*6*8 = 384 for going second

This policy will create the new board positions as it goes.

Usually, it will run greedy play,
but the explore variable is the chance (out of 1) that it will explore.

The learning rate determines how fast it learns.
It decreases to 0 as the policy player learns so that the values converge.

Remember, the policy player only changes the probabilities up through its last...
explore move (or all the way through if there was no explore move)
'''

#I need a way to represent the policy for a board
#A way to create a new policy based on a board position
#an architecture for storing all the policies
#A way to remember which values to back up

class Policy:
    def __init__(self, openSpaces = range(9)):
        self.values = {}
        self.subpolicies = {}
        self.openSpaces = openSpaces
        for openSpace in self.openSpaces:
            self.values[openSpace] = .5
    
    def __str__(self):
        return str(self.values)+" with subpolicies for "+ str([policyNum for policyNum in self.subpolicies])
    
    def __delitem__(self, key):
        self.subpolicies.__delitem__(key)
    #Will throw a KeyError if it's not there
    def __getitem__(self, key):
        return self.subpolicies.__getitem__(key)
    def __setitem__(self, key, value):
        self.subpolicies.__setitem__(key, value)
    
    #If explore is false, return the greedy (highest) value in this policy
    #If explore is true, choose a random value that's not the greedy one
    def suggest(self, explore = False):
        greedyIndex = max(self.values, key=self.values.get)
        greedy = self.values[greedyIndex]
        greedyIndexes = [index for index in self.values if self.values[index]==greedy]
        if explore:
            return random.choice([index for index in self.values if not (index in greedyIndexes)])
        else:
            return random.choice(greedyIndexes)
            
    def addSubpolicy(self, index):
        self.subpolicies[index] = Policy([openSpace for openSpace in self.openSpaces if openSpace!=index])
    
    #the formula used is old = old+learningRate*(target-old)
    def update(self, value, target, learningRate):
        self.values[value]+=learningRate*(target-self.values[value])


class PolicyPlayer:
    def __init__(self, exploreRate = 0, learningRate = 1):
        self.policy = Policy()
    
    #takes the game
    def makeMove(self, game, me):
        trace = []
        curPolicy = self.policy 
        for move in game.movesMade():
            moveNumber = move[0]
            trace.append(moveNumber)
            try:
                policy = curPolicy[moveNumber] #get the policy for that move
            except KeyError:
                self.policy.addSubpolicy(moveNumber)
                curPolicy = curPolicy[moveNumber]
        explore = random.random()<self.exploreRate
            
        

if __name__ == "__main__":
    p = Policy()
    p.values = {1:3, 2:4, 6:1, 9:10, 7:10, 5:10}
    print(p)
    p.update(1, 10, .5)
    print(p)
    p.addSubpolicy(1)
    print(p[1])
    print(p)