#a very basic game class
class Game():
    #TODO change all these to Google-style docstrings
    """
    Determine who has won the game
    
    Returns
        None if game is not finished yet, -1 if game is a tie, 
        or the winning player's number if there's a winner
    """
    def whoWon(self):
        raise NotImplementedError
    
    """
    Get the player number of the other player
    
    Args
        curPlayerNum: The number of a player
    
    Returns
        The player number of another player
    """
    def getOtherPlayerNum(self, curPlayerNum):
        raise NotImplementedError
    
    #return a list of all the possible moves available to the player
    #Moves do not necessarily have to be a number here, they could anything=
    def getPossibleMoves(self, playerNum):
        raise NotImplementedError
    
    #TODO this used to be static
    #run an interface to allow a human to make a move in the game
    def makeHumanMove(self, playerNum):
        raise NotImplementedError
    
    #TODO this used to be static
    #make a random move in the game
    def makeRandomMove(self, playerNum):
        raise NotImplementedError
    
    #make the move @move with player @playerNum
    def makeMove(self, move, playerNum):
        raise NotImplementedError
    
    