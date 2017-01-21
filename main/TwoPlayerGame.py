'''
TwoPlayerGame is an abstract class (with the occasional pre-implemented method)
...for any two player game where the game has a state
...and players can make moves (represented by numbers or strings).
If all of the methods are implemented, a PolicyPlayer can learn to play the game.
'''
import random

class IllegalMove(RuntimeError):
    pass

#abstract class for a two player game
class TwoPlayerGame:
    def __init__(self):
        self.pastMoves = []
    
    #Convert the state of this game into a unique string
    #If two games are in the same state, they should return the same string
    #
    #Although this string technically could be used to recreate the game,
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
    def undoMove(self):
        raise NotImplementedError
        
    #Returns a new game object that's a copy of the old one but with the player numbers swapped
    #(If player 1 made a move in the current game, the returned game will have player -1 make that move and vice versa)
    def getReversedPlayers(self):
        #dps
        ans = self.__class__() #create an empty copy of the game
        #go through the game moves
        for move in self.pastMoves:
            ans.makeMove(move[0], -move[1]) #make the same move with the opposite player
        return ans
        
    #situation: return value
    #game is not finished: None
    #tie game: 0
    #player 1 won: 1
    #player -1 won: -1
    def whoWon(self):
        raise NotImplementedError
    
    @staticmethod
    def makeRandomMove(game, player):
        game.makeMove(random.choice(game.getPossibleMoves(player = player)), player)

    @staticmethod
    def makeHumanMove(game, player):
        print("Your options are: {}".format(game.getPossibleMoves(player = player)))
        while True:
            try:
                playerMove = input("Where would you like to go? ")
                try:
                    playerMove = int(playerMove)
                except ValueError: #if the string can't be converted to an int
                    pass
                game.makeMove(playerMove, player)
                break #the move was successful, so break out of the while loop and return
            except:
                print("That didn't seem to work.")
                


class TwoPlayerGamePlayer:
    #gameClasses is a list of classes you want the TwoPlayerGamePlayer to be able to play.
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
    #If one of the players is 'human' then comment is automatically set to 1
    def play(self, who = ("random", "random"), gameClassIndex = 0, comment = 0, gameParameters = None):
        gameClass = self.gameClasses[gameClassIndex]
        whoToFunction = {"random":gameClass.makeRandomMove, "human":gameClass.makeHumanMove}
        #the functions that should be called when that player wants to move
        #the first value stays None (so that we can have index 1 and -1 be different)
        #the function at index 1 is for player 1
        #the function at index 2 (or -1) is for player -1
        functions = [None, None, None]
        for playerNum, player in enumerate(who):
            if player=='human':
                comment = 1
            if isinstance(player, str):
                functions[playerNum+1] = whoToFunction[player]
            else: #any class with a "makeMove(game, curPlayer)" function
                functions[playerNum+1] = player.makeMove
        curPlayer = random.choice([-1, 1])
        
        if gameParameters == None:
            gameParameters = [] #default
        #create the game to play
        game = gameClass(*gameParameters)
        if comment:
            print("New game!")
        while game.whoWon()==None:
            if comment:
                print(game)
                #uses 1 instead of -1 as a player number
                #uses 2 instead of 1 as a player number
                print("Player {}'s turn!".format(((curPlayer+1)//2)+1)) 
            functions[curPlayer](game, curPlayer) #run the function to have the player make their move
            curPlayer*=-1 #other player's turn
        if comment:
            print(game)
            winner = game.whoWon()
            
            if winner==1:
                print("Player 2 wins!")
            elif winner==-1:
                print("Player 1 wins!")
            else:
                print("Tie game!")
        return game