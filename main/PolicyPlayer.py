import random
import sys
import UsefulThings as useful
import Testers as test
import TicTacToeGame as tttg
import LogicalPlayer as lp #TODO used for testing
import OldPolicyPlayer as opp #TODO used for testing


assert sys.version_info[0] >= 3, "Python version needs to be at least 3"
'''
Policy Player

Creates a policy for each position on the board.

A policy consists of a dictionary of 9 values, each representing a probability
...of winning if you take that spot

A complete policy would hold 3^9 = 19683 different board positions.
But that would include impossible positions, so there are actually less board positions.

This policy will create policies for new board positions as it goes.

Usually, it will run greedy play,
but the explore variable is the chance (out of 1) that it will explore.

The learning rate determines how fast it learns.

Remember, the policy player only changes the probabilities up through its last
...explore move (or all the way through if there was no explore move)
'''

class UncreatablePolicy(RuntimeError):
    def __init__(self):
        RuntimeError.__init__("Was not given a board with which to create a new policy.")

#basically just a fancy dict that stores the value of choosing each action at a particular state
#It can suggest values to choose and be greedy (choose its 'best' option) or
#...have a probability of exploring (choosing a 'non-best' option)
class Policy:
    #openSpaces is a list of options that are actually choosable
    #defaultValue is the default value for choosing each action
    def __init__(self, openSpaces = range(9), defaultValue = .5):
        self.values = {} #the dict to store the value of choosing each action
        self.openSpaces = openSpaces
        for openSpace in self.openSpaces:
            self.values[openSpace] = defaultValue
    
    def __str__(self):
        return str(self.values)
    
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
    
    #the formula used is
    #old = old+learningRate*(target-old)
    #This moves old a fraction (learningRate) closer to the target.
    #If learningRate is 1, it moves it to the target.
    #If learningRate is 0, it does nothing.
    def update(self, value, target, learningRate):
        self.values[value]+=learningRate*(target-self.values[value])


class PolicyPlayer:
    @staticmethod
    def convertBoardToString(board):
        ans = ""
        for index, value in enumerate(board):
            ans+=str(index)+str(value)
        return ans
            
    
    def __init__(self, exploreRate = 0, learningRate = 1, rewards = [0, 1, 1], defaultPolicyValue = .5):
        self.rewards = rewards #reward for [loss, tie, win]
        self.policies = {}
        self.exploreRate = exploreRate
        self.learningRate = learningRate
        self.defaultPolicyValue = defaultPolicyValue
        #[game, playerNumber, exploreMoves]
        #exploreMoves is a list of the moves that were explore moves in the most recent game it played.
        #...0 corresponds to the first move.
        self.curGameInfo = [None, None, []] 

    #takes the game (game), and the player number of the policy player (me)
    #makes a move in the game based on its policies and exploreRate 
    def makeMove(self, game, me):
        #if the player is not assigned 1, make it 1 when evaluating the position
        if me==-1:
            policy = self.getPolicy(game.getConvert())
        else: #me==1
            policy = self.getPolicy(game)
            
        explore = random.random()<self.exploreRate
        moveIndex = len(game.movesMade)
        if game!=self.curGameInfo[0]: #new game; rewrite self.curGameInfo
            self.curGameInfo = [game, me, []]
        if explore: #add the explore move to the exploreMoves list
            self.curGameInfo[2].append(moveIndex)
        game.makeMove(policy.suggest(explore = explore), me)
        
    #Given a game or string representation of a game, returns the policy for that game position
    #Creates policies for positions it hasn't explored yet
    def getPolicy(self, game):
        if isinstance(game, str):#given the string representation of a board
            try:
                return self.policies[game] #get the policy
            except:
                raise RuntimeError("Could not find a policy with string code '{}'".format(game))
        else: #given an actual game
            try:
                stringIndex = self.convertBoardToString(game.board) #cache in case of KeyError
                return self.policies[stringIndex] #get the policy for that move
            except KeyError: #this policy doesn't exist yet
                return self.addPolicy(game, stringIndex) #make and get the new policy
                
    #takes a game (with a game board)
    #creates a new empty policy based on the board
    #The policy does not include impossible moves
    #returns the new policy that was added to the game
    #If there is a policy already there, it will overwrite it.
    #If provided, stringIndex should be self.convertBoardToString(game.board)
    def addPolicy(self, game, stringIndex = None):
        #If it hasn't been given, compute stringIndex
        if stringIndex is None:
            stringIndex = self.convertBoardToString(game.board)
        #add the policy to the policies property with the string version of the board as the index to reach it
        policy = Policy(openSpaces = game.getOpenSpaces(), defaultValue = self.defaultPolicyValue)
        self.policies[stringIndex] = policy
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
        #dp
        #print("ExploreMoves: {}".format(exploreMoves))
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
        #from this point on, I don't use the game to tell me what player is making the move
        #...I base it on @param wentLast.
        #So, I can convert the game so the policy player is player 1
        #...and not run into any issues later on
        if me==-1:
            game = game.getConvert()
        else:
            #I will be editing the board, so I need to copy the game
            game = game.copy()
        
        #there's a move at the end the policy player doesn't care about    
        if not wentLast:
            game.undoMove()
        #dp
        #print("wentLast: {}".format(wentLast))
        updateVal = reward
        movesMadeLen = len(game.movesMade) #cache
        #while I haven't gone through all the moves I need to and
        #I'm not trying to update for any move that occured before an explore move
        while movesMadeLen>0 and (not movesMadeLen+1 in exploreMoves):
            #dp
            #print("movesMadeLen at start: {}".format(movesMadeLen))
            #the particular move we're updating
            move = game.undoMove()[0]
            #the value dict of the policy we're updating
            policyValues = self.getPolicy(game).values
            #the previous, or 'past' value of that move
            pastVal = policyValues[move]
            #do the update
            updateVal = pastVal + self.learningRate*(updateVal - pastVal)
            policyValues[move] = updateVal
            #dp
            #print(policyValues)
            #go to the next move
            try:
                game.undoMove()
            except IndexError:
                #len(game.movesMade)==0,
                #...so instead of breaking at the start of the loop,
                #just have it break here
                break 
            movesMadeLen = len(game.movesMade) #cache
            #dp
            #print(movesMadeLen)
            

if __name__ == "__main__":
    import TicTacToeGame as tttg
    import timeit
    '''
    p = PolicyPlayer(exploreRate = .5, learningRate = .5, rewards = [0, 1, 3])
    for i in range(3):
        g = tttg.play(who = (p, 'random'))
        print(g)
        print(g.movesMade)
        p.update()
    p.exploreRate = 0
    while True:
        tttg.play(who = (p, "human"))
    '''
    
    print("Working...")
    winnerList = []
    while True:
        exploreRate, learningRate, rewards = (0, .5, [-3, 0, 5])
        gamesToPlay = 150000
        playerNumber = 1
        
        p = PolicyPlayer(exploreRate = exploreRate, learningRate = learningRate, rewards = rewards)
        playAgainst = 'random'
        for i in range(gamesToPlay):
                useful.printPercent(i, gamesToPlay, 5, 1)
                g = tttg.play(who = (playAgainst, p))
                p.update()
        p.exploreRate = 0
        pctIncrement = 10
        results = test.testAgainstRandom(p, comment = 0, pctIncrement = pctIncrement)
        print("Player {} done.".format(playerNumber))
        print("Winners without most recent player included: {}".format(winnerList))
        
        while results[1][0]>0:
            playerNumber+=1
            p = PolicyPlayer(exploreRate = exploreRate, learningRate = learningRate, rewards = rewards)
            playAgainst = 'random'
            for i in range(gamesToPlay):
                    useful.printPercent(i, gamesToPlay, 5, 1)
                    g = tttg.play(who = (playAgainst, p))
                    p.update()
            p.exploreRate = 0
            pctIncrement = 10
            results = test.testAgainstRandom(p, comment = 0, pctIncrement = pctIncrement)
            print("Player {} done.".format(playerNumber))
            print("Winners without most recent player included: {}".format(winnerList))
    
        print("Player number {} is a winner!".format(playerNumber))
        winnerList.append(playerNumber)
    #while True:
    #    tttg.play(who = ('human', p))
    '''
    for times in range(5):
        for i in range(gamesToPlay):
            #useful.printPercent(i, gamesToPlay, 25, 1)
            g = tttg.play(who = (playAgainst, p))
            p.update()
        pctIncrement = 0
        p.exploreRate = 0
        test.testAgainstRandom(p, comment = 0, pctIncrement = pctIncrement)
        
        p = opp.OldPolicyPlayer(exploreRate = exploreRate, learningRate = learningRate, rewards = rewards)
        for i in range(gamesToPlay):
            #useful.printPercent(i, gamesToPlay, 25, 1)
            g = tttg.play(who = (playAgainst, p))
            p.update()
        p.exploreRate = 0
        test.testAgainstRandom(p, comment = 0, pctIncrement = pctIncrement)
    '''
    
    '''
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
    '''
    print("Second training!")
    playAgainst = 'random'
    p.rewards = [-10, 1, 1]
    for i in range(gamesToPlay):
        useful.printPercent(i, gamesToPlay, 5, 1)
        g = tttg.play(who = (playAgainst, p))
        p.update()
    '''
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
    '''