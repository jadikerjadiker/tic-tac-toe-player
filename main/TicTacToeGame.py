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
        
    def __str__(self):
        def convertToStr(num):
            if num==0:
                return '-'
            elif num==1:
                return 'O'
            elif num==-1:
                return 'X'
            else:
                raise RuntimeError("Unrecognized symbol in game: '{}'".format(num))
            
        ans = ""
        for i, val in enumerate(self.board):
            ans+=convertToStr(val)+" "
            if i%3==2: #if we just added the last symbol for the row
                ans+='\n'

        return ans
            
            
        #return ("Game:{}".format(self.board))
        
    def reset(self):
        self.__init__()
        
    def makeMove(self, where, playerNum):
        assert playerNum==1 or playerNum==-1, "Players can only play 1 or -1, not '{}'".format(playerNum)
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
    
    #returns a new game object that's a copy of the old one but with the player numbers swapped
    def getConvert(self):
        ans = TicTacToeGame() #make a new game to return, don't edit the old one
        #redo the game with the conversion
        for move in self.movesMade:
            #convert the value, using the original if no conversion is listed
            ans.makeMove(move[0], -move[1])
        return ans
        
    #returns a copy of the game
    def copy(self):
        ans = TicTacToeGame()
        #just redo the game from the start on a new game
        for move in self.movesMade:
            ans.makeMove(*move)
        return ans

#just a slightly faster method than play(who = ('random', 'random'))
#often times random games are used for training so we want this to be fast.
def makeRandomGame():
    game = TicTacToeGame()
    player = 1
    while game.whoWon()==None:
        makeRandomMove(game, player)
        player*=-1
    
    return game

def makeRandomMove(game, player):
    game.makeMove(random.choice(game.getOpenSpaces()), player)

def makeHumanMove(game, player):
    while True:
        try:
            if player==1:
                print("You are O")
            else:
                print("You are X")
            game.makeMove(int(raw_input("Where would you like to go? "))-1, player)
            break
        except:
            print("That didn't seem to work.")

#who is a tuple (player1, player-1)
#each of the players can either be:
#'random': random player
#'human': ask the human to make a move
#net: pass in a neural net with the method "makeMove(game, player)" to make the move
def play(who = ("random", "random"), comment = 0):
    whoToFunction = {"random":makeRandomMove, "human":makeHumanMove}
    #the functions that should be called when that player wants to move
    #the first value stays None (so that we can have index 1 and -1 be different)
    #the value at index 1 is for player 1
    #the value at index 2 (or -1) is for player -1
    functions = [None, None, None]
    for playerNum, player in enumerate(who):
        if player=='human':
            comment = 1
        if isinstance(player, str):
            functions[playerNum+1] = whoToFunction[player]
        else: #net or any other class with a "makeMove" function
            functions[playerNum+1] = player.makeMove
    curPlayer = random.choice([-1, 1])
    game = TicTacToeGame()
    if comment:
        print("New game!")
    while game.whoWon()==None:
        if comment:
            print(game)
        functions[curPlayer](game, curPlayer) #run the function to have the player make their move
        curPlayer*=-1 #other player's turn
    if comment:
        print(game)
        winner = game.whoWon()
        if winner==1:
            print("O wins!")
        elif winner==-1:
            print("X wins!")
        else:
            print("Tie game!")
    return game
                
                
if __name__=="__main__":
    while True:
        print(play(('random', 'random')))
    