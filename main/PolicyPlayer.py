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
        self.rewards = [0, 1, 1] #reward for [loss, tie, win]
        self.policy = Policy()
        self.exploreRate = exploreRate
        self.learningRate = learningRate
        #[game, playerNumber, exploreMoves]
        #exploreMoves is a list of the moves that were explore moves in the most recent game it played.
        #...0 corresponds to the first move.
        self.curGameInfo = [None, None, []] 

    #takes the game
    def makeMove(self, game, me):
        policy = self.getPolicy([move[0] for move in game.movesMade])
        explore = random.random()<self.exploreRate
        moveIndex = len(game.movesMade)
        if moveIndex<=1: #new game; rewrite self.curGameInfo
            self.curGameInfo = [game, me, []]
        if explore: #add the explore move to the exploreMoves list
            self.curGameInfo[2].append(moveIndex)
        game.makeMove(policy.suggest(explore = explore), me)
        
    #given a list of move positions made in a game (index 0 of a move)
    #...returns the policy for that list
    #Creates policies for positions it hasn't explored yet
    def getPolicy(self, moveList):
        policy = self.policy
        for move in moveList:
            try:
                policy = policy[move] #get the policy for that move
            except KeyError: #this policy doesn't exist yet
                policy.addSubpolicy(move) #make the new policy
                policy = policy[move] #get the new policy
                
        return policy
    
    #Updates the policies based on the gameInfo
    #Only updates for one player in the game
    #gameInfo should be in the form [game, me, exploreMoves]
    #game is the game you want it to update with
    #me is the player you want it to update as
    #exploreMoves is a list of exploratory moves made by the player
    #...where 1 corresponds to the second move in the game
    def update(self, gameInfo = None):
        if gameInfo is None:
            gameInfo = self.curGameInfo
        game, me, exploreMoves = gameInfo
        winner = game.whoWon()
        wentLast = False #whether or not I made the last move in the game
        rewardIndex = 0 #index to get value from self.rewards, default to loss
        if winner == me: #updating from a  win
            rewardIndex = 2
            wentLast = True
        elif winner == 0: #tie
            rewardIndex = 1
            wentLast = None #can't tell if I went last yet
        reward = self.rewards[rewardIndex]
        if wentLast==None:
            #check the last move and see if I was the one who made it
            wentLast = game.movesMade[-1][1]==me
        
        trace = [moveAndPlayer[0] for moveAndPlayer in game.movesMade] #get a list of the moves made in the game
        if not wentLast:
            trace = trace[:-1]
        updateVal = reward
        
        while len(trace)>0:
            #the value dict of the policy we're updating
            policyValues = self.getPolicy(trace[:-1]).values
            #the particular move we're updating
            move = trace[-1]
            #the previous, or 'past' value of that move
            pastVal = policyValues[move]
            #do the update
            updateVal = pastVal + self.learningRate*(updateVal - pastVal)
            policyValues[move] = updateVal
            #go to the next move
            trace = trace[:-2] #this will not raise an exception if trace is too small
            
        
if __name__ == "__main__":
    import TicTacToeGame as tttg
    import timeit
    #timeit.timeit(stmt = "for i in range(100): g = tttg.play(who = ('random', p));p.update()")
    p = PolicyPlayer(exploreRate = 0, learningRate = .5)
    gamesToPlay = 100000
    for i in range(gamesToPlay):
        print("Playing game {}/{}".format(i+1, gamesToPlay))
        g = tttg.play(who = ('random', p))
        p.update()
    while True:
        tttg.play(who = ("human", p))