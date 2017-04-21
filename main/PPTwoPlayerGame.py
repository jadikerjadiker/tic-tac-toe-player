import random

'''
PPTwoPlayerGame is an abstract class (with the occasional pre-implemented method)
...for any two player game where the game has a state
...and players can make moves (represented by numbers or strings).
If all of the methods are implemented, a Player can learn to play the game.
'''

class IllegalMove(RuntimeError):
    pass

#abstract class for a two player game
class PPTwoPlayerGame:
    def __init__(self):
        self.pastMoves = []
    
    #Get the number of the other player in the game (1 or 0 respectively)
    @staticmethod
    def getOtherPlayerNum(playerNum):
        return (playerNum+1)%2
    
    #Make a random move in the game
    @staticmethod
    def makeRandomMove(game, playerNum):
        game.makeMove(random.choice(game.getPossibleMoves(playerNum = playerNum)), playerNum)
    
    #Interface for a human to make a move in the game.
    #This is usually overriden in the subclass
    @staticmethod
    def makeHumanMove(game, playerNum):
        print("Your options are: {}".format(game.getPossibleMoves(playerNum = playerNum)))
        while True:
            try:
                playerMove = input("Where would you like to go? ")
                try:
                    playerMove = int(playerMove)
                except ValueError: #if the string can't be converted to an int
                    pass
                game.makeMove(playerMove, playerNum)
                break #the move was successful, so break out of the while loop and return
            except:
                print("That didn't seem to work.")
                
    
    #Convert the state of this game into a unique string
    #If two games are in the same state, they should return the same string
    #
    #Although it should technically be possible to recreate the game
    #(at least in its current state) using the returned string
    #it does not have to be easy to recreate the game
    #from the string returned by this function
    #
    #This is completely separate from __str__()
    def convertToStr(self):
        raise NotImplementedError
     
    #Much like convertToStr except
    #instead of converting into a string, you convert into a constant-sized list
    #Constant-sized means that this function must always return a list of the same size
    def convertToConstLenList(self):
        raise NotImplementedError
    
    #Returns a list of possible moves that one could make, given the current game position
    #Each move needs to be a string or a number 
    def getPossibleMoves(self, playerNum):
        raise NotImplementedError
    
    #Makes a move in the game and adds the move and playerNum as a tuple to the list self.pastMoves
    #playerNum is the name of the player making the move
    #move is an object which determines how to make the move
    #Raises IllegalMove if the move is illegal
    #Does not return anything
    def makeMove(self, move, playerNum):
        self.pastMoves.append((move, playerNum))
        raise NotImplementedError
        
    #Undoes the most recent move in the game
    #Better implementations of this function may include a 'moveIndex' variable
    #that allows the undo of a particular move or bring the state of the game
    #back to that particular move
    #returns the last full move ((move, playerNum)) that was made
    def undoMove(self):
        #return move
        raise NotImplementedError
       
    def copy(self):
        ans = self.__class__() #create empty game of same type
        for move in self.pastMoves:
            ans.makeMove(move[0], move[1]) #make the same move with the opposite player
        return ans
     
    #Returns a new game object that's a copy of the old one but with the player numbers swapped
    #(If player 1 made a move in the current game, the returned game will have player -1 make that move and vice versa)
    def getReversedPlayers(self):
        ans = self.__class__() #create an empty game of same type
        #go through the game moves
        for move in self.pastMoves:
            ans.makeMove(move[0], self.getOtherPlayerNum(move[1])) #make the same move with the opposite player
        return ans
        
    #situation: return value
    #game is not finished: None
    #tie game: 0
    #player 1 won: 1
    #player -1 won: -1
    def whoWon(self):
        raise NotImplementedError


class PPTwoPlayerGamePlayer:
    #gameClasses is a list of classes you want the PPTwoPlayerGamePlayer to be able to play.
    #They will be assigned the same index they have inside gameClasses
    def __init__(self, gameClasses):
        self.gameClasses = []
        if not hasattr(gameClasses, "__iter__"):
            #it used to be a single class, so now we're just making it into a list
            gameClasses = [gameClasses]
        #add the game class to the list
        for gameClass in gameClasses:
            self.gameClasses.append(gameClass)
            
    #who is a tuple (player 1, player -1)
    #each of the players can either be:
    #'random': random player
    #'human': ask the human to make a move
    #an object: pass in an object with the method "makeMove(game, player)" to make a move in the game
    #gameClassIndex is the index of the game class you want it to play.
    #comment is an integer. The higher the integer, the more info the function will print.
    #gameParameters is a tuple ([listOfNonKeywordArgs], {dictOfKewordArgs}) to pass to the init of the game when playing it.
    #If one of the players is 'human' then comment is automatically set to 1
    def play(self, who = ("random", "random"), gameClassIndex = 0, comment = 0, gameParameters = None):
        gameClass = self.gameClasses[gameClassIndex]
        whoToFunction = {"random":gameClass.makeRandomMove, "human":gameClass.makeHumanMove}
        #the functions that should be called when that player wants to move
        #update: use list comprehension here
        functions = []
        for index, player in enumerate(who):
            if isinstance(player, str):
                functions.append(whoToFunction[who[index]])
                if player=="human" and comment<1:
                    comment = 1
            else: #player is an object with a "makeMove" method
                functions.append(player.makeMove)
                
        curPlayerNum = random.choice([0, 1])
        
        if gameParameters == None:
            gameParameters = ([], {}) #default
        #create the game to play
        game = gameClass(*gameParameters[0], **gameParameters[1])
        if comment:
            print("New game!")
        while game.whoWon()==None:
            if comment:
                print("\n"+str(game))
                #uses 1 instead of -1 as a player number
                #uses 2 instead of 1 as a player number
                print("Player {}'s turn!".format(curPlayerNum+1)) #converting it to human numbers (starting at 1) before printing
            functions[curPlayerNum](game, curPlayerNum) #run the function to have the player make their move
            if comment:
                print("Player {} moved.".format(curPlayerNum+1)) #converting it to human numbers (starting at 1) before printing
            curPlayerNum = game.getOtherPlayerNum(curPlayerNum) #other player's turn
        if comment:
            print("\n"+str(game))
            winner = game.whoWon()
            
            if winner==0:
                print("Player 1 wins!")
            elif winner==1:
                print("Player 2 wins!")
            else:
                print("Tie game!")
        return game
        
if __name__ == "__main__":
    import UsefulThings as useful
    import ChopsticksGame as cg
    gamePlayer = PPTwoPlayerGamePlayer(cg.ChopsticksGame)
    while True:
        gamePlayer.play(who = ('human', 'human'))
        if useful.askYesOrNo("Play again?"):
            break
    