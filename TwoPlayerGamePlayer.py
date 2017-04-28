import random


#TODO make sure I can delete PPTwoPlayerGame after this, and if so, then delete it.
#basic super class for game players
#these are players who actually make moves in the game and (potentially) learn from the games
class TwoPlayerGamePlayer():
    def makeMove(self):
        raise NotImplementedError
        
    def update(self):
        raise NotImplementedError

#used to actually run a game between two different players    
class TwoPlayerGameRunner():
    #gameClasses is a list of subclasses of Game that you want to be able to run.
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