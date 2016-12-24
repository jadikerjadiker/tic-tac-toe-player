import Game
import copy

'''
Input: a finished two-player tic-tac-toe game with a winner
Output:
a list of tuples [(gameState, responseOfWinner), (gameState, responseOfWinner), etc.]

gameState = [-1,-1, 0, 0, 0, 1, 0, 0, 1] where a -1 is the opponenent, and 1 is the winning player
responseOfWinner = [0, 0, 1, 0, 0, 0, 0, 0, 0], a one-hot where the 1 is where the winning player chose to move.
(in this case, the winner is going in the top right of the gameboard, blocking the opponenent's win, and winning down the right side)

'''
def makeTrainingSet(game):
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
    
if __name__ == "__main__":
    g = Game.Game()
    g.makeMove(0, 18)
    g.makeMove(5, 23)
    g.makeMove(3, 18)
    g.makeMove(6, 23)
    g.makeMove(1, 18)
    g.makeMove(7, 23)
    g.makeMove(2, 18)
    h = makeTrainingSet(g)
    print(g)
    print(h)