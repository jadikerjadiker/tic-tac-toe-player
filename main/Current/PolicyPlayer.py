import random
import UsefulThings as useful
import Testers as test
import pickle
from Policy import Policy, UncreatablePolicy, NonExistantPolicy

useful.assertPython3()

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

class PolicyPlayer:
    def __init__(self, exploreRate = 0, learningRate = 1, rewards = None, defaultPolicyValue = .5):
        if rewards is None:
            rewards = [0, .5, 1] #default
        self.rewards = rewards #reward for [loss, tie, win]
        self.policies = {} #{stringRepresentingGame: PolicyForGame, ...}
        self.exploreRate = exploreRate
        self.learningRate = learningRate
        self.defaultPolicyValue = defaultPolicyValue
        #[game, playerNumber, exploreMoves]
        #exploreMoves is a list of the moves that were explore moves in the most recent game it played.
        #...0 corresponds to the first move.
        self.curGameInfo = [None, None, []]
    
    #Save the policies this player has learned
    #The fileName should have the extension '.pkl'
    def save(self, fileName):
        with open(fileName, 'wb') as f:
            pickle.dump(self.policies, f, pickle.HIGHEST_PROTOCOL)
    
    #load the policies this player has learned      
    def load(self, fileName):
        with open(fileName, 'rb') as f:
            self.policies = pickle.load(f)

    #Takes the game (game), and the player number of the policy player (me)
    #Makes a move in the game based on its policies and exploreRate
    #Note that the PolicyPlayer always stores policies such that it's the one making the move for Player 0
    #So if it's playing as player 1, it will need to look up (and store) the policy with "myGame = game.getReversedPlayers()""
    #...instead of "game"
    def makeMove(self, game, me):
        #if the player is not assigned 1, make it 1 when evaluating the position
        myGame = game
        if me==1:
            myGame = game.getReversedPlayers()
        
        try:
            policy = self.getPolicy(myGame)
        except NonExistantPolicy:
            policy = self.getPolicy(myGame, myGame.getPossibleMoves(playerNum = 0))
            
        explore = random.random()<self.exploreRate
        moveIndex = len(myGame.pastMoves)
        if game!=self.curGameInfo[0]: #new game; rewrite self.curGameInfo
            self.curGameInfo = [game, me, []] #[game, playerNumber, exploreMoves]
        if explore: #add the explore move to the exploreMoves list
            self.curGameInfo[2].append(moveIndex)
        game.makeMove(policy.suggest(explore = explore), me)
      
    #Given a game or string representation of a game, returns the policy for that game position
    #If a policy for that position does not yet exist and it is given possibleMoves (a list of moves that are available in the position),
    #...it will create (using addPolicy) a new policy and return that new policy
    #If a policy for that position does not yet exist and it is not given possibleMoves, it raises a NonExistantPolicy error
    def getPolicy(self, game, possibleMoves = None):
        if isinstance(game, str):#given the string representation of a board
            try:
                return self.policies[game] #get the policy
            except:
                raise NonExistantPolicy("Could not find a policy with string code '{}'".format(game))
        else: #given an actual game
            try:
                stringIndex = game.convertToStr() #cache in case of KeyError
                return self.policies[stringIndex] #get the policy for that move
            except KeyError: #this policy doesn't exist yet
                if possibleMoves:
                    return self.addPolicy(game, possibleMoves)
                raise NonExistantPolicy

    #takes a game, and creates a new empty policy for it
    #The policy only has actions for those listed in "possibleMoves"
    #Returns the new policy that was added to the player
    #If there is a policy already there, it will overwrite it, so be careful.
    #If provided, stringIndex should be game.convertToStr()
    #stringIndex is provided as a parameter because often times a function that
    #...is calling addPolicy will already have computed game.convertToStr()
    #...so it can just pass it instead of having addPolicy() recompute it
    def addPolicy(self, game, possibleMoves, stringIndex = None):
        #If it hasn't been given, compute stringIndex
        if stringIndex is None:
            stringIndex = game.convertToStr()
        #add the policy to the policies property with the string version of the board as the index to reach it
        policy = Policy(possActions = possibleMoves, defaultValue = self.defaultPolicyValue)
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
        winner = game.whoWon()
        wentLast = (game.pastMoves[-1][1] == me) #whether or not I made the last move in the game
        rewardIndex = 0 #index to get value from self.rewards, default to loss
        if winner == me: #updating from a  win
            rewardIndex = 2
        elif winner == -1: #tie
            rewardIndex = 1
        reward = self.rewards[rewardIndex]
        if wentLast==None:
            #check the last move and see if I was the one who made it
            wentLast = game.pastMoves[-1][1]==me
        #from this point on, I don't use the game to tell me what player is making the move
        #...I base it on @param wentLast.
        #So, I can convert the game so the policy player is player 0
        #...and not run into any issues later on
        if me==1:
            game = game.getReversedPlayers()
        else:
            #I will be editing the board, so I need to copy the game
            game = game.copy()
        
        #there's a move at the end the policy player doesn't care about    
        if not wentLast:
            game.undoMove()
        #note that this is just setting the initial value
        updateVal = reward
        pastMovesLen = len(game.pastMoves) #cache
        #while I haven't gone through all the moves I need to and
        #I'm not trying to update for any move that occured before an explore move
        while pastMovesLen>0 and (not pastMovesLen+1 in exploreMoves):
            #the particular move we're updating
            move, playerNum = game.undoMove()
            #the value dict of the policy we're updating
            policyValues = self.getPolicy(game).values #we will need a "myGame" here
            #the previous, or 'past' value of that move
            pastVal = policyValues[move]
            #do the update
            updateVal = pastVal + self.learningRate*(updateVal - pastVal)
            #update val carries on to the next update we do for this game
            policyValues[move] = updateVal
            #go to the next move
            try:
                game.undoMove()
            except IndexError:
                #len(game.pastMoves)==0,
                #...so instead of breaking at the start of the loop,
                #just have it break here
                break 
            pastMovesLen = len(game.pastMoves) #cache
            

if __name__ == "__main__":
    from PPTwoPlayerGame import PPTwoPlayerGamePlayer
    from ChopsticksGame import ChopsticksGame
    from ChopsticksOverAndOutGame import ChopsticksOverAndOutGame
    from TicTacToeGame import TicTacToeGame
    import LogicalPlayer as lp
    
    
    print("Working...")
    
    '''
    gameClass = TicTacToeGame
    gamePlayer = PPTwoPlayerGamePlayer(gameClass)
    gameParameters =  ([], {}) #default
    exploreRate, learningRate, rewards = (0, 1, [1, 2, 1])
    learner = PolicyPlayer(exploreRate = exploreRate, learningRate = learningRate, rewards = rewards)
    
    while True:
        gamePlayer.play(who = ('human', learner))
        learner.update()
        for policyIndex in learner.policies:
            print("Index: {}\nPolicy: {}".format(policyIndex, learner.policies[policyIndex]))
    
    
    '''
    
    p = PolicyPlayer(exploreRate = 0, learningRate = .5, rewards = [-5000, 1, 10])
    gameClass = ChopsticksGame
    gamePlayer = PPTwoPlayerGamePlayer(gameClass)
    gamesToPlay = 10000
    #p.load("saved.pkl")
    for i in range(gamesToPlay):
        useful.printPercent(i, gamesToPlay, 5, 1)
        g = gamePlayer.play(who = (p, 'random'))
        p.update()
    
    p.exploreRate = 0
    test.testAgainstRandom(p, gameClass)
    #p.save("saved.pkl")
    while True:
        gamePlayer.play(who = (p, "human"))
    
    
    '''
    print("Working...")
    gameClass = TicTacToeGame
    gamePlayer = PPTwoPlayerGamePlayer(gameClass)
    gameParameters =  ([], {}) #default
    gamesPerRound = 10000 #default. Often overriden later.
    printOneGamePer = 0
    exploreRate, learningRate, rewards = (.01, .5, [-1000, 1, 10])
    saveFile = "myPolicies.json"
    '''
    '''
    if gameClass==ChopsticksGame:
        gameParameters =  ([], {"state":None, "tieLimit":3})
        exploreRate, learningRate, rewards = (0, .5, [-10000, 1, 10])
        gamesPerRound = 2000
    '''
    '''
    p = PolicyPlayer(exploreRate = exploreRate, learningRate = learningRate, rewards = rewards)
    p2 = PolicyPlayer(exploreRate = exploreRate, learningRate = learningRate, rewards = rewards)
    while True:
        p.exploreRate = exploreRate
        p2.exploreRate = exploreRate
        for i in range(gamesPerRound):
            useful.printPercent(i, gamesPerRound, 5, 1)
            gamePlayer.play(who = (p, 'random'), gameParameters = gameParameters)
            gamePlayer.play(who = (p2, 'random'), gameParameters = gameParameters)
            p.update()
            p2.update()
        for i in range(gamesPerRound):
                useful.printPercent(i, gamesPerRound, 5, 1)
                g = gamePlayer.play(who = (p, p2), gameParameters = gameParameters)
                p.update()
                p2.update()
                if printOneGamePer and i%printOneGamePer==0:
                    print(g)
                    print(g.pastMoves)
    '''
    '''          
        #p.exploreRate = 0
        #p2.exploreRate = 0
        pctIncrement = 10
        p.exploreRate = 0
        p2.exploreRate = 0
        test.testAgainstRandom(p, gameClass, gamesPerRound = 100, rounds = 25, comment = 0, pctIncrement = pctIncrement)
        test.testAgainstRandom(p2, gameClass, gamesPerRound = 100, rounds = 25, comment = 0, pctIncrement = pctIncrement)

        if useful.askYesOrNo("Would you like to play p?"):
            while True:
                gamePlayer.play(who = ('human', p), gameParameters = gameParameters)
                if not useful.askYesOrNo("Play again?"):
                    break
                
        if useful.askYesOrNo("Would you like to play p2?"):
            while True:
                gamePlayer.play(who = ('human', p2), gameParameters = gameParameters)
                if not useful.askYesOrNo("Play again?"):
                    break
    '''
    
    
    '''
    print("Working...")
    winnerList = []
    gameClass = TicTacToeGame
    gamePlayer = PPTwoPlayerGamePlayer(gameClass)
    gameParameters =  ([], {}) #default
    gamesToPlay = 10000 #default. Often overriden later.
    exploreRate, learningRate, rewards = (0, .5, [-10000, 1, 10])
    playAgainst = 'random'
    saveFile = "myPolicies.json"
    if gameClass==ChopsticksGame:
        gameParameters =  ([], {"state":None, "tieLimit":3})
        exploreRate, learningRate, rewards = (0, .5, [-10000, 1, 10])
        gamesToPlay = 20000
    
    while True:
        p = PolicyPlayer(exploreRate = exploreRate, learningRate = learningRate, rewards = rewards)
        for i in range(gamesToPlay):
                useful.printPercent(i, gamesToPlay, 5, 1)
                g = gamePlayer.play(who = (playAgainst, p), gameParameters = gameParameters)
                p.update()
        p.exploreRate = 0
        pctIncrement = 10
        results = test.testAgainstRandom(p, gameClass, gamesPerRound = 100, rounds = 25, comment = 0, pctIncrement = pctIncrement)
        
        #p.save(saveFile)
        
        if useful.askYesOrNo("Would you like to play it?"):
            while True:
                gamePlayer.play(who = ('human', p), gameParameters = gameParameters)
                if not useful.askYesOrNo("Play again?"):
                    break
    '''
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