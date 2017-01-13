class IllegalMove(RuntimeError):
    pass

#abstract class for a two player game
class TwoPlayerGame:
    def __init__(self):
        pass
    
    #situation: return value
    #game is not finished: None
    #tie game: 0
    #player 1 won: 1
    #player -1 won: -1
    def whoWon(self):
        raise NotImplementedError
        
    #Makes a move in the game,
    #playerNum is the name of the player making the move
    #move is an object which determines how to make the move
    #Raises IllegalMove if the move is illegal
    #Does not return anything
    def makeMove(self, move, playerNum):
        raise NotImplementedError
    