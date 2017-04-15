import random
import sys
import UsefulThings as useful
import Testers as test
import LogicalPlayer as lp #TODO used for testing
import TicTacToeGame as tttg

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
            try:
                return random.choice([index for index in self.values if not (index in greedyIndexes)])
            #if all the values are greedy
            #just skip over this and choose a random greedy one
            except IndexError:
                pass
        return random.choice(greedyIndexes)
            
    def addSubpolicy(self, index):
        self.subpolicies[index] = Policy([openSpace for openSpace in self.openSpaces if openSpace!=index])
    
    #the formula used is old = old+learningRate*(target-old)
    def update(self, value, target, learningRate):
        self.values[value]+=learningRate*(target-self.values[value])
        
class OldPolicyPlayer:
    def __init__(self, exploreRate = 0, learningRate = 1, rewards = [0, 1, 1]):
        self.rewards = rewards #reward for [loss, tie, win]
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
        if game!=self.curGameInfo[0]: #new game; rewrite self.curGameInfo
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
        
        while len(trace)>0 and (not ((len(trace)+1) in exploreMoves)):
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
        