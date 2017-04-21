import random
import UsefulThings as useful
from PPTwoPlayerGame import IllegalMove, PPTwoPlayerGame
from PPWithNNTwoPlayerGame import PPWithNNTwoPlayerGame
from overrides import overrides
useful.assertPython3()

'''
A class that allows for the simulation and playing of a tic-tac-toe game
'''
class TicTacToeGame(PPWithNNTwoPlayerGame):
    @classmethod
    #just a slightly faster method than PPTwoPlayerGamePlayer(TicTacToeGame).play(who = ('random', 'random'))
    #often times random games are used for training so we want this to be fast.
    def makeRandomGame(Cls):
        game = Cls()
        playerNum = 0
        while game.whoWon()==None:
            Cls.makeRandomMove(game, playerNum)
            playerNum = Cls.getOtherPlayerNum(playerNum)
        return game
    
    #The decorators must be in this order or it won't work.   
    @staticmethod
    @overrides
    def makeHumanMove(game, player):
        while True:
            try:
                if player==0:
                    print("You are O")
                else: #player===1
                    print("You are X")
                move = int(input("Where would you like to go? "))-1
                if move>8 or move<0:
                    raise IllegalMove()
                game.makeMove(move, player)
                break
            except:
                print("That didn't seem to work.")
    
    def __init__(self):
        PPTwoPlayerGame.__init__(self)
        #-1 is an empty slot on the board
        #0 is a player, and 1 is the other player.
        self.board = [-1]*9
        
        #will be in the form [(where, who), (where, who), etc.]
        #where "where" is position of placement and "who" is number used to represent player
        self.pastMoves = []
        
    def __str__(self):
        def toStr(num):
            if num==-1:
                return '-'
            elif num==0:
                return 'O'
            elif num==1:
                return 'X'
            else:
                raise RuntimeError("Unrecognized symbol in game: '{}'".format(num))
        #main
        ans = ""
        for i, val in enumerate(self.board):
            ans+=toStr(val)+" "
            if i%3==2: #if we just added the last symbol for the row
                ans+='\n'

        return ans
    
    @overrides
    def convertToStr(self):
        ans = ""
        for value in self.board:
            #the space at the end takes up a little more space,
            #but allows strToConstLenList to go faster
            ans+=str(value)+" "
        return ans
        
    @overrides
    #The strings are always a string of integers, so this should just turn it into a list.
    def strToConstLenList(self, string):
        return [int(num) for num in string.split()]
    
    @overrides
    def makeMove(self, where, playerNum):
        assert playerNum==0 or playerNum==1, "Players can only play 0 or 1, not '{}'".format(playerNum)
        if self.board[where]==-1:
            self.board[where] = playerNum
            self.pastMoves.append((where, playerNum))
        else:
            raise IllegalMove("Cannot make move at '{}' by player '{}' because it is already taken. {}".format(where, playerNum, self))
    
    @overrides
    #undoes the move with index 'moveIndex' and returns it
    #if moveIndex is unspecified, it defaults to the last move made
    def undoMove(self, moveIndex = None):
        if moveIndex is None:
            moveIndex = len(self.pastMoves)-1
        #remove (and also get) the move from the pastMoves list
        move = self.pastMoves.pop(moveIndex)
        self.board[move[0]]=-1 #undo the move
        return move
        
    @overrides
    #determines who won the game, if anyone
    #returns None if no one has won the game and the game is not over yet
    #returns -1 if the game is a tie
    #returns the number of the person who won if there is a winner
    #upgrade: I think this function can be simplified. A lot of what's going on in the diagonal checking is the exact same as the straight line checking.
    def whoWon(self):
        if -1 in self.board: #game is not done, default to unfinished
            ans = None
        else: #game is done, default to tie
            ans = -1
        #first check the rows for winning, then check diagonals
        runningVal = None
        for checking in range(4):
            for i in range(3):
                if checking<2: #checking rows and columns
                    for j in range(3):
                        if checking==0: #checking rows
                            val = self.board[i*3+j]
                        else: #checking columns
                            val = self.board[i+j*3]
                        
                        if val==-1: #person doesn't have the row or column
                            break
                        else:
                            if j==0: #if it just started checking this line
                                runningVal = val
                            elif not val==runningVal: #if the person doesn't have a win
                                break
                            elif j==2:
                                return runningVal
                else: #checking diagonals
                    if checking==2:
                        val = self.board[i*4] #want it to check 0, 4, 8
                    else: #checking==3
                        val = self.board[(i+1)*2] #want it to check 2, 4, 6
                        
                    if val==-1: #person doesn't have the row or column
                        break
                    else:
                        if i==0: #if we're just checking this diagonal
                            runningVal = val
                        elif not val==runningVal: #if the person doesn't have a win
                            break
                        elif i==2:
                            return runningVal
            
        return ans
    
    
    
    @overrides
    #returns a list of the open spaces on the board
    #upgrade: might be faster as a property
    #upgrade: can be written as a list comprehension
    def getPossibleMoves(self, playerNum = None):
        ans = []
        for i, val in enumerate(self.board):
            if val==-1:
                ans.append(i)
        return ans
        
    #returns a copy of the game
    def copy(self):
        ans = TicTacToeGame()
        #just redo the game from the start on a new game
        for move in self.pastMoves:
            ans.makeMove(*move)
        return ans
                
    
                
if __name__=="__main__":
    from PPTwoPlayerGame import PPTwoPlayerGamePlayer
    game = TicTacToeGame()
    gamePlayer = PPTwoPlayerGamePlayer(TicTacToeGame)
    for i in range(4):
        game = TicTacToeGame.makeRandomGame()
        s = game.convertToStr()
        print("s: {}".format(s))
        print("back: {}".format(game.strToConstLenList(s)))
    while True:
        gamePlayer.play(who = ('human', 'human'))
        s = game.convertToStr()
        print("s: {}".format(s))
        print("back: {}".format(game.strToConstLenList(s)))
    