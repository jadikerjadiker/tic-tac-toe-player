#Old Tic Tac Toe Trainers
import NeuralNet
import TicTacToeGame as tttg
import random

'''
First strategy:
Create random games and play as the winner.
Train on x amount of these games (where there actually is a winner)
'''
class LearningNet1(NeuralNet.NeuralNet):
    def __init__(self, architecture, trainingGameAmt = 100, learningRate = 5, trainingMode = ('error', .0001)):
        NeuralNet.NeuralNet.__init__(self, architecture)
        self.trainingGameAmt = trainingGameAmt
        self.learningRate = learningRate
        self.trainingModeType, self.trainingModeValue = trainingMode
        self.version = 1
     
    '''
    Input: a finished two-player tic-tac-toe game with a winner
    Output:
    a list of tuples [(gameState, responseOfWinner), (gameState, responseOfWinner), etc.]
    
    gameState = [-1,-1, 0, 0, 0, 1, 0, 0, 1] where a -1 is the opponenent, and 1 is the winning player
    responseOfWinner = [0, 0, 1, 0, 0, 0, 0, 0, 0], a one-hot vector/list where the 1 is where the winning player chose to move.
    (in this case, the winner is going in the top right of the gameboard, blocking the opponenent's win, and winning down the right side)
    
    '''   
    def makeTrainingSet(self, game):
        winner = game.whoWon()
        assert winner, "There must be a winner of the game in order to make a training set out of it. Here is the game:\n{}".format(game)
        ans = []
        
        #this section of code changes the numbers within the game to be -1, 0, and 1
        #1 is the winner, and -1 is the loser (opponent)
        conversion = {0:0}
        player1 = game.movesMade[0][1]
        winnerGoesFirst = True
        if player1==winner:
            conversion[player1] = 1
            conversion[game.movesMade[1][1]] = -1 #opponent
        else:
            conversion[player1] = -1 #opponent
            conversion[game.movesMade[1][1]] = 1
            winnerGoesFirst = False
            
        #TODO the games have a function to do this on their own now
        normalGame = tttg.TicTacToeGame() #make a copy of this old game that has the -1, 0, and 1 as the numbers
        for move in game.movesMade:
            normalGame.makeMove(move[0], conversion[move[1]])
        
        trainingGame = tttg.TicTacToeGame()
        
        myMove = False
        if winnerGoesFirst:
            myMove = True
        
        for move in normalGame.movesMade:
            if myMove:
                oneHotMove = [0]*9
                oneHotMove[move[0]] = 1
                ans.append(([val for val in trainingGame.board], oneHotMove)) #TODO delete if this works
            trainingGame.makeMove(*move)
            myMove = not myMove
                
        return ans
    
    #trains itself to play as the winner in self.trainingGameAmt games with winners
    #uses self.learningRate and self.iterations to control the training
    def autoTrain(self, comment = False):
        for gameNumber in range(self.trainingGameAmt):
            if comment:
                print("Training game {}/{}".format(gameNumber+1, self.trainingGameAmt))
            #make a random game with a winner
            game = tttg.makeRandomGame()
            while not game.whoWon(): #while nobody has won the game
                game = tttg.makeRandomGame()
            if comment:
                print(game)
            trainingSet = self.makeTrainingSet(game)
            self.train(trainingSet, learningRate = self.learningRate, mode = (self.trainingModeType, self.trainingModeValue))
        if comment:
            print("Autotraining complete!")
    
    #takes a game, the player number of this player and the player number of the opponent
    #returns the move this net makes
    def getMove(self, game, me, opponent):
        myGame = game.getConvert({me:1, opponent:-1})
        responses = list(self.run(myGame.board))
        openSpaces = game.getOpenSpaces()
        assert len(openSpaces)>0, "The game must not be finished/full in order for the computer to make a move."
        topVal = -1 #default val because it's impossible (it's negative)
        ans = None
        for openSpace in openSpaces:
            if responses[openSpace]>topVal:
                topVal = responses[openSpace]
                ans = openSpace
        return ans
    
    #not using 'run' until I can figure out the naming thing. TODO
    def go(self, comment = False):
        self.autoTrain(comment)


'''
Second strategy:
Play against a human and learn from those games.
'''
class LearningNet2(NeuralNet.NeuralNet):
    def __init__(self, architecture, learningRate = 5, trainingMode = ('error', .0001)):
        NeuralNet.NeuralNet.__init__(self, architecture)
        self.learningRate = learningRate
        self.trainingModeType, self.trainingModeValue = trainingMode
        self.version = 2
     
    '''
    Input: a finished two-player tic-tac-toe game
    Output:
    If the game has a winner, then the output is:
        a list of tuples [(gameState, responseOfWinner), (gameState, responseOfWinner), etc.]
    
    If the game is a tie, then the output is:
        a list of tuples [(gameState, responseOfPlayer1), (gameState, responseOfPlayer1), etc., (gameState, responseOfPlayer2), (gameState, responseOfPlayer2), etc.]
    
    gameState = [-1,-1, 0, 0, 0, 1, 0, 0, 1] where a -1 is the opponenent, and 1 is the winning player
    responseOfPlayer or responseOfWinner = [0, 0, 1, 0, 0, 0, 0, 0, 0], a one-hot vector/list where the 1 is where the winning player chose to move.
    (in this case, the player is going in the top right of the gameboard, blocking the opponenent's win, and winning down the right side)
    
    '''   
    def makeTrainingSet(self, game):
        winner = game.whoWon()
        assert winner!=None, "The game must be finished in order to make a training set out of it. Here is the game:\n{}".format(game)
        ans = []
        trainingGame = tttg.TicTacToeGame()
        if winner:
            myMove = (winner==game.movesMade[0][1])
        else:
            myMove = (1==game.movesMade[0][1])
        for move in game.movesMade:
            if myMove:
                oneHotMove = [0]*9
                oneHotMove[move[0]] = 1
                ans.append(([boardSpace for boardSpace in trainingGame.board], oneHotMove))
            elif winner==0:
                print("Other player board:\n{}".format(trainingGame.board))
                oneHotMove = [0]*9
                oneHotMove[move[0]] = 1
                ans.append(([-boardSpace for boardSpace in trainingGame.board], oneHotMove)) #reverse the players
            trainingGame.makeMove(*move)
            myMove = not myMove #next player's move
        return ans
        
    #takes a game, the player number of this player and the player number of the opponent
    #returns the move this net makes
    def getMove(self, game, me = 1, opponent = -1):
        myGame = game.getConvert({me:1, opponent:-1})
        responses = list(self.run(myGame.board))
        openSpaces = game.getOpenSpaces()
        assert len(openSpaces)>0, "The game must not be finished/full in order for the computer to make a move."
        topVal = -1 #default val because it's impossible (it's negative)
        ans = None
        for openSpace in openSpaces:
            if responses[openSpace]>topVal:
                topVal = responses[openSpace]
                ans = openSpace
        return ans
    
    #not using 'run' until I can figure out the naming thing. TODO
    def go(self, comment = False):
        while True:
            game = tttg.playHumanVNeuralNet(self)
            if game.whoWon():
                self.train(self.makeTrainingSet(game), learningRate = self.learningRate, mode = (self.trainingModeType, self.trainingModeValue))


'''
Third strategy:
Have the neural net play against random nets and then learn from those games.
'''
class LearningNet3(NeuralNet.NeuralNet):
    def __init__(self, architecture, learningRate = 1, trainingMode = ('avg', .01), examplesPerBatch = 10):
        NeuralNet.NeuralNet.__init__(self, architecture, learningRate = learningRate, trainingMode = trainingMode)
        self.examplesPerBatch = examplesPerBatch #TODO see if this should be moved to NeuralNet
        self.version = 3
    
    '''
    Input: a list of finished two-player tic-tac-toe games or a single finished two-player tic-tac-toe game.
    Output:
    If there are only games with a winner, then the output is:
        a list of tuples [(game1State1, responseOfWinner), (game1State3, responseOfWinner), etc.]
    
    If there are only tie games, then the output is:
        a list of tuples [(game1State1, responseOfPlayer1), (game1State3, responseOfPlayer1), etc., (game1State2, responseOfPlayer2), (game1State4, responseOfPlayer2), etc.]
        
    And if there's both, then it will look something like:
        a list of tuples [(game1State1, responseOfWinner), etc., (game1State1, responseOfPlayer1), etc., (game1State2, responseOfPlayer2), etc.]
    
    gameState = [-1,-1, 0, 0, 0, 1, 0, 0, 1] where a -1 is the opponenent, and 1 is the winning player
    responseOfPlayer or responseOfWinner = [0, 0, 1, 0, 0, 0, 0, 0, 0], a one-hot vector/list where the 1 is where the winning player chose to move.
    (in this case, the player is going in the top right of the gameboard, blocking the opponenent's win, and winning down the right side)
    
    '''   
    def makeTrainingSet(self, gameList, examplesPerBatch = None):
        if examplesPerBatch==None:
            examplesPerBatch = -1
        ans = []
        batch = []
        batchCountdown = examplesPerBatch
        if not hasattr(gameList, "__iter__"):
            gameList = [gameList] #it used to be a single game, so now we're just making it into a list
        for game in gameList:
            winner = game.whoWon()
            assert winner!=None, "The game must be finished in order to make a training set out of it. Here is the game:\n{}".format(game)
            
            #make sure the winner is 1 so the game board doesn't have to be reversed when making the training examples
            if winner and winner==-1:
                game = game.getConvert()
                
            trainingGame = tttg.TicTacToeGame()
            #The computer is always considered to be 1 for the training sets
            #see if player 1 goes first
            myMove = (1==game.movesMade[0][1])
            for move in game.movesMade:
                #if we've added the right amount of games to the batch
                if batchCountdown==0:
                    ans.append(batch) #add the batch to the final training set
                    batch = [] #this actually reassigns batch to a new list, not overwriting the old one
                    batchCountdown = examplesPerBatch #reset the counter
                if myMove: #if player 1 is going
                    oneHotMove = [0]*9
                    oneHotMove[move[0]] = 1
                    batch.append(([boardSpace for boardSpace in trainingGame.board], oneHotMove))
                    batchCountdown-=1
                elif winner==0: #if the game's a tie, train for the other player as well
                    oneHotMove = [0]*9
                    oneHotMove[move[0]] = 1
                    #reverse the players on the board so it looks like it's player 1's turn
                    batch.append(([-boardSpace for boardSpace in trainingGame.board], oneHotMove))
                    batchCountdown-=1
                trainingGame.makeMove(*move)
                myMove = not myMove #next player's move
        if len(batch)>0:
            ans.append(batch)
        return ans
        
    #takes a game, the player number of this player and the player number of the opponent
    #returns the move this net makes
    def getMove(self, game, me = 1):
        #make sure I'm player 1 when I make the move
        if me==-1:
            myGame = game.getConvert()
        else:
            myGame = game
        responses = list(self.run(myGame.board))
        openSpaces = myGame.getOpenSpaces()
        assert len(openSpaces)>0, "The game must not be finished/full in order for the computer to make a move."
        topVal = -1 #default val because it's impossible (it's negative)
        ans = None
        for openSpace in openSpaces:
            if responses[openSpace]>topVal:
                topVal = responses[openSpace]
                ans = openSpace
        return ans
        
    def makeMove(self, game, player):
        game.makeMove(self.getMove(game, player), player)
    
    def go(self, gamesPerRound = 100, rounds = 5, comment = False, playAfterRound = False):
        games = []
        for roundNum in range(rounds):
            for gameNum in range(gamesPerRound):
                games.append(tttg.play(who = (self, 'random')))
            #for game in games:
            #    print(game)
            if comment>1:
                print("Training Round {}...".format(roundNum+1))
            self.train(self.makeTrainingSet(games, examplesPerBatch = self.examplesPerBatch), learningRate = self.learningRate, mode = self.trainingMode, comment = comment-1)
            if comment>1:
                print("Training complete!")
                print("Testing against random nets.")
            testAgainstRandom(self, games = 1000, comment = comment)
            #TODO add in "Sorry, I couldn't understand that" type stuff
            if playAfterRound:
                if askYesOrNo("Would you like to play against the net?"):
                    while True:
                        tttg.play(('human', self))
                        if not askYesOrNo("Would you like to play again?"):
                            break
        if comment>0:
            print("All training is complete!")
        if playAfterRound:
            print("You can just play now.")
            while True:
                tttg.play(('human', self))

def askYesOrNo(question):
    while True:
        try:
            ans = raw_input(question+" (y/n) ").lower()
            if ans in ['y', 'yes', 'yeah', 'yep']:
                return True
            elif ans in ['n', 'no', 'nope']:
                return False
            else:
                raise RuntimeError("Bad input")
        except:
            print("Answer was not 'y' or 'n'.")

def testAgainstRandom(net, games = 100, comment = False):
    results = [0]*3 #[losses, ties, wins] for the net
    for gameNum in range(games):
        if comment>0:
            print("Testing game {}/{}".format((gameNum+1), games))
        game = tttg.TicTacToeGame()
        player = random.choice([1, -1])
        while game.whoWon()==None:
            if player==1:
                net.makeMove(game, 1)
            else: #player==-1
                tttg.makeRandomMove(game, -1)
            player*=-1
            
        results[game.whoWon()+1]+=1
        if comment>1:
            if comment>2:
                print(game)
            print("Results so far:\n{}".format(results))
    if comment>0:
        print("Final results:\n{}".format(results))
    return results

if __name__ == '__main__':
    
    #Testing range of error for playing against random nets
    net = LearningNet3([9, 9, 9, 9], learningRate = .0001, trainingMode = ('avgAvg', .198), examplesPerBatch = None)
    net.go(gamesPerRound = 1000, rounds = 1, comment = 3)
    testRuns = 50
    gamesPerTest = 1000
    lows = [gamesPerTest+1]*3
    highs = [-1]*3
    overall = [0]*3
    for i in range(testRuns):
        test = testAgainstRandom(net, games = gamesPerTest)
        for j, testVal in enumerate(test):
            lows[j] = min(lows[j], testVal)
            highs[j] = max(highs[j], testVal)
            overall[j]+=testVal
        print(test)
    ranges = [highs[i]-lows[i] for i in range(3)]
    print("Lows: {}".format(lows))
    print("Highs: {}".format(highs))
    print("Ranges: {}".format(ranges))
    avgs = [overall[i]*1.0/testRuns for i in range(3)] #the *1.0 makes it so it doesn't use integer division 
    print("Averages: {}".format(avgs))

    '''
    #Training workhorse
    response = [0]*9
    for i in range(100):
        sky = LearningNet1([9, 9, 9, 9, 9], trainingGameAmt = 1000, learningRate = 1, trainingMode = ('error', .01))
        sky.go(comment = False)
        game = tttg.TicTacToeGame()
        response[sky.getMove(game, 1, -1)]+=1
        print("RESPONSE {}: {}".format(i+1, response))
    print(response)
    '''
   