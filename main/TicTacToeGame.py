import random

class IllegalMove(RuntimeError):
    pass

class TicTacToeGame:
    def __init__(self):
        #0 is an empty slot on the board
        #It is usually the case (but it is not assumed) that 1 is a player, -1 is the other player.
        self.board = [0]*9
        
        #will be in the form [(where, who), (where, who), etc.]
        #where "where" is position of placement and "who" is number used to represent player
        self.movesMade = []
        
    #todo this can be made so much better
    def __str__(self):
        def convertToStr(num):
            if num==0:
                return '-'
            elif num==1:
                return 'O'
            elif num==-1:
                return 'X'
            else:
                return str(num)
            
        ans = ""
        spaceLen = max([len(str(val)) for val in self.board])
        for i, val in enumerate(self.board):
            strVal = convertToStr(val)
            ans+=strVal+" "*(spaceLen+1-len(strVal))
        
            if i%3==2:
                ans+='\n'

        return ans
            
            
        #return ("Game:{}".format(self.board))
        
    def reset(self):
        self.__init__()
        
    def makeMove(self, where, playerNum):
        if self.board[where]==0:
            self.board[where] = playerNum
            self.movesMade.append((where, playerNum))
            
        else:
            raise IllegalMove("Cannot make move at '{}' by player '{}' because it is already taken. {}".format(where, playerNum, self))
    
    #determines who won the game, if anyone
    #returns None if no one has won the game and the game is not over yet
    #returns 0 if the game is a tie
    #returns the number of the person who won if there is a winner
    #todo I think this function can be simplified. A lot of what's gonig on in the diagonal checking is the exact same as the straight line checking.
    def whoWon(self):
        if 0 in self.board: #game is not done
            ans = None
        else: #game is done
            ans = 0
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
                        
                        if val==0: #person doesn't have the row or column
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
                        
                    if val==0: #person doesn't have the row or column
                        break
                    else:
                        if i==0: #if we're just checking this diagonal
                            runningVal = val
                        elif not val==runningVal: #if the person doesn't have a win
                            break
                        elif i==2:
                            return runningVal
            
        return ans
    
    def getOpenSpaces(self):
        ans = []
        for i, val in enumerate(self.board):
            if val==0:
                ans.append(i)
        return ans
    
    #returns a new game with the players in the game converted to certain numbers
    #conversion is a dictionary with keys being the old player number,
    #and the values being the number it should be converted to    
    def getConvert(self, conversion):
        ans = TicTacToeGame() #make a new game to return, don't edit the old one
        #redo the game with the conversion
        for move in self.movesMade:
            #convert the value, using the original if no conversion is listed
            ans.makeMove(move[0], conversion.get(move[1], move[1]))
        return ans
        
    #converts the players in the game to certain numbers
    #conversion is a dictionary with keys being the old player number,
    #and the values being the number it should be converted to 
    #does not return anything
    def convert(self, conversion):
        self = self.getConvert(conversion)
    
    #returns a copy of the game
    def copy(self):
        ans = TicTacToeGame()
        #just redo the game from the start on a new game
        for move in self.movesMade:
            ans.makeMove(*move)
        return ans
                        
def makeRandomGame():
    game = TicTacToeGame()
    player = 1
    while game.whoWon()==None:
        game.makeMove(random.choice(game.getOpenSpaces()), player)
        player*=-1
    
    return game