import random
import sys
import UsefulThings as useful
import Testers as test
import LogicalPlayer as lp #TODO used for testing


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


class PolicyPlayer:
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
            
        
if __name__ == "__main__":
    import TicTacToeGame as tttg
    import timeit
    #timeit.timeit(stmt = "for i in range(100): g = tttg.play(who = ('random', p));p.update()")
    pctIncrement = 5
    p = PolicyPlayer(exploreRate = .15, learningRate = .5, rewards = [-10, 1, 3])
    p2 = PolicyPlayer(exploreRate = .1, learningRate = .5, rewards = [0, 1, 3])
    gamesToPlay = 250000
    playAgainst = 'random'
    for i in range(gamesToPlay):
        useful.printPercent(i, gamesToPlay, 5, 1)
        g = tttg.play(who = (playAgainst, p))
        p.update()
    print("Training second policy player")
    for i in range(gamesToPlay):
        useful.printPercent(i, gamesToPlay, 5, 1)
        g = tttg.play(who = (playAgainst, p2))
        p2.update()
    print("Testing before they play each other")
    test.testAgainstRandom(p, comment = 0, pctIncrement = pctIncrement)
    test.testAgainstRandom(p2, comment = 0, pctIncrement = pctIncrement)
    playAgainst = p2
    for i in range(gamesToPlay):
        useful.printPercent(i, gamesToPlay, 5, 1)
        g = tttg.play(who = (playAgainst, p))
        p.update()
        p2.update()
        #p.curGameInfo[2]*=-1
        #p.update()
    print("Testing after they've played eachother")
    '''
    print("Second training!")
    playAgainst = 'random'
    p.rewards = [-10, 1, 1]
    for i in range(gamesToPlay):
        useful.printPercent(i, gamesToPlay, 5, 1)
        g = tttg.play(who = (playAgainst, p))
        p.update()
    '''
    print("Testing against random player...")
    #test.testAgainstRandom(p, comment = 0, pctIncrement = pctIncrement)
    p.exploreRate = 0
    p2.exploreRate = 0
    test.testAgainstRandom(p, comment = 0, pctIncrement = pctIncrement)
    test.testAgainstRandom(p2, comment = 0, pctIncrement = pctIncrement)
    while True:
        print("Playing p")
        tttg.play(who = ("human", p))
        print("Playing p1")
        tttg.play(who = ("human", p2))