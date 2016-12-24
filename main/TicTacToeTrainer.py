import NeuralNet
import TicTacToeGame as tttg
import random

'''
The goal of this is to create a neural network that will learn how to play tic-tac-toe.

Things to fool around with:
Training "away" from losing
How many games in each training batch
Net architecture
Training as random winner versus playing against random player

Things I could fool around with:
Regularization
Learning rate
'''

'''
Third strategy:
Have the neural net play against random nets and then learn from those games.
'''
class LearningNet3(NeuralNet.NeuralNet):
    def __init__(self, architecture, learningRate = 5, trainingMode = ('error', .0001)):
        NeuralNet.NeuralNet.__init__(self, architecture)
        self.learningRate = learningRate
        self.trainingModeType, self.trainingModeValue = trainingMode
        self.version = 3
     
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
    def makeTrainingSet(self, gameList, gamesPerBatch):
        winner = game.whoWon()
        assert winner!=None, "The game must be finished in order to make a training set out of it. Here is the game:\n{}".format(game)
        ans = []
        for game in gameList:
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
    
    def go(self, comment = False):
        while True:
            game = tttg.playHumanVNeuralNet(self)
            if game.whoWon():
                self.train(self.makeTrainingSet(game), learningRate = self.learningRate, mode = (self.trainingModeType, self.trainingModeValue))

def testAgainstRandom(net, games = 100, comment = False):
    results = [0]*3 #[losses, ties, wins] for the net
    for gameNum in range(games):
        if comment:
            print("Testing game {}/{}".format((gameNum+1), games))
        game = tttg.TicTacToeGame()
        player = random.choice([1, -1])
        while game.whoWon()==None:
            if player==1:
                game.makeMove(net.getMove(game, 1, -1), 1)
            else: #player==-1
                tttg.makeRandomMove(game, -1)
            player*=-1
            
        results[game.whoWon()+1]+=1
        if comment:
            print(game)
            print("Results so far:\n{}".format(results))
    return results
            
                
  
if __name__ == '__main__':
    
    '''
    #Testing range of error for playing against random nets
    net = LearningNet1([9, 9, 9, 9], learningRate = 1, trainingMode = ('error', .001), trainingGameAmt = 1000)
    net.go()
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
        