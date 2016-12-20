import NeuralNet
import TicTacToeGame as tttg

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
First strategy:
Create random games and play as the winner.
Train on x amount of these games (where there actually is a winner)
Then, play against human and learn from those games.
'''
import Game
import copy

class LearningNet1(NeuralNet.NeuralNet):
    def __init__(self, architecture, trainingGameAmt = 100, learningRate = 5, iterations = 100):
        NeuralNet.NeuralNet.__init__(self, architecture)
        self.trainingGameAmt = trainingGameAmt
        self.learningRate = learningRate
        self.iterations = iterations
     
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
            
        normalGame = Game.Game() #make a copy of this old game that has the -1, 0, and 1 as the numbers
        for move in game.movesMade:
            normalGame.makeMove(move[0], conversion[move[1]])
        
        trainingGame = Game.Game()
        
        myMove = False
        if winnerGoesFirst:
            myMove = True
        
        for move in normalGame.movesMade:
            if myMove:
                oneHotMove = [0]*9
                oneHotMove[move[0]] = 1
                ans.append((copy.copy(trainingGame.board), oneHotMove))
            trainingGame.makeMove(*move)
            myMove = not myMove
                
        return ans
    
    #trains itself to play as the winner in self.trainingGameAmt games with winners
    #uses self.learningRate and self.iterations to control the training
    def autoTrain(self):
        for gameNumber in range(self.trainingGameAmt):
            print("Training game {}/{}".format(gameNumber+1, self.trainingGameAmt))
            #make a random game with a winner
            game = tttg.makeRandomGame()
            while not game.whoWon(): #while nobody has won the game
                game = tttg.makeRandomGame()
            
            trainingSet = self.makeTrainingSet(game)
            self.train(trainingSet, learningRate = self.learningRate, iterations = self.iterations)
        print("Autotraining complete!")
    
    #takes a game, the player number of this player and the player number of the opponent
    #returns the move this net makes
    def getMove(self, game, me, opponent):
        def makeOneHotMove(val):
            ans = [0]*9
            ans[val] = 1
            return ans
            
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
        return makeOneHotMove(ans)
    
    #not using 'run' until I can figure out the naming thing. TODO
    def go(self):
        self.autoTrain()

    
    
if __name__ == '__main__':
    sky = LearningNet1([9, 9, 9, 9], trainingGameAmt = 50)
    #sky.go()
    game = tttg.TicTacToeGame()
    game.makeMove(0, 5)
    game.makeMove(2, 5)
    print(game)
    print(sky.run(game.getConvert({5:-1}).board))

    print(sky.getMove(game, 1, 5))
        
    