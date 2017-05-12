#basic super class for game players
#these are players who actually make moves in the game and (potentially) learn from the games
class TwoPlayerGamePlayer():
    def makeMove(self):
        raise NotImplementedError
        
    def update(self):
        raise NotImplementedError