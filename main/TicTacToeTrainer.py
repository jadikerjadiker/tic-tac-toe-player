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
    
    def go(self, gamesPerRound = 100, rounds = 5, comment = False):
        games = []
        for roundNum in range(rounds):
            for gameNum in range(gamesPerRound):
                games.append(tttg.play(who = (self, 'random')))
            for game in games:
                print(game)
            print("Training Round {}...".format(roundNum+1))
            self.train(self.makeTrainingSet(games, examplesPerBatch = self.examplesPerBatch), learningRate = self.learningRate, mode = self.trainingMode, comment = True)
            print("Training complete!")
            #TODO add in "Sorry, I couldn't understand that" stuff
            if raw_input("Would you like to play against the net? (y/n) ").lower()=='y':
                while True:
                    tttg.play(('human', net))
                    if raw_input("Would you like to play again? (y/n) ").lower()=='n':
                        break
        print("All training is complete! You can just play now.")
        while True:
            tttg.play(('human', 'human'))
            

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
    #TODO fix the error amount changes based on what I set it to.
    net = LearningNet3([9, 9, 9, 9], learningRate = .1, trainingMode = ('avgAvg', .125))
    net.go()
    '''
    net = LearningNet3([9, 9, 9, 9], learningRate = .01, trainingMode = ('avgAvg', .01))
    #game = tttg.playHumanVRandom()
    trainingSet = []
    for i in range(100):
        trainingSet.append(tttg.makeRandomGame())
    trainingSet = net.makeTrainingSet(trainingSet)
    print(trainingSet)
    print("Training started")
    net.train(trainingSet, comment = True)
    print("Training ended")
    '''
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
        