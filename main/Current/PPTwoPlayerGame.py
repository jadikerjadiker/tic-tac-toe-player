import random
from TwoPlayerGame import TwoPlayerGame
from TwoPlayerGameRunner import TwoPlayerGameRunner

'''
PPTwoPlayerGame is an abstract class (with the occasional pre-implemented method)
...for any two player game where the game has a state
...and players can make moves (represented by numbers or strings).
If all of the methods are implemented, a Player can learn to play the game.
'''
#TODO decide if I'm going to do NotImplementedError or ABCMeta and stick with it for all classes
class IllegalMove(RuntimeError):
    pass

#abstract class for a two player game
class PPTwoPlayerGame(TwoPlayerGame):
    def __init__(self):
        self.pastMoves = []
    
    #Get the number of the other player in the game (1 or 0 respectively)
    def getOtherPlayerNum(self, playerNum):
        return (playerNum+1)%2
    
    #Make a random move in the game
    def makeRandomMove(self, playerNum):
        self.makeMove(random.choice(self.getPossibleMoves(playerNum = playerNum)), playerNum)
    
    #Interface for a human to make a move in the game.
    #This is usually overriden in the subclass
    def makeHumanMove(self, playerNum):
        print("Your options are: {}".format(self.getPossibleMoves(playerNum = playerNum)))
        while True:
            try:
                playerMove = input("Where would you like to go? ")
                try:
                    playerMove = int(playerMove)
                except ValueError: #if the string can't be converted to an int
                    pass
                self.makeMove(playerMove, playerNum)
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



        
if __name__ == "__main__":
    import UsefulThings as useful
    import ChopsticksGame as cg
    gamePlayer = TwoPlayerGameRunner(cg.ChopsticksGame)
    while True:
        gamePlayer.play(who = ('human', 'human'))
        if not useful.askYesOrNo("Play again?"):
            break
    