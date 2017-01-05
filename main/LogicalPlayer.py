import TicTacToeGame as tttg
import random

'''
A player that will always win when it has the option
and will always block the opponent when it has the option.
Otherwise, it does a random move
'''
class LogicalPlayer:
    #get the logical players move
    def getMove(self, game, me):
        moveToBlock = -1
        possMoves = game.getOpenSpaces()
        for move in possMoves:
            myGame = game.copy()
            myGame.makeMove(move, me)
            #If this move makes me win me the game, return it
            if myGame.whoWon()==me:
                return move
            myGame = game.copy()
            myGame.makeMove(move, -me) #pretend I'm the other player
            if myGame.whoWon()==-me:
                moveToBlock = move
        #it can't win, so it should at least block
        if moveToBlock>-1:
            return moveToBlock
        else: #make random move
            return random.choice(possMoves)
            
    def makeMove(self, game, me):
        game.makeMove(self.getMove(game, me), me)

            
if __name__ == "__main__":
    for game in range(20):
        tttg.play(who=(LogicalPlayer(), LogicalPlayer()), comment = 1)