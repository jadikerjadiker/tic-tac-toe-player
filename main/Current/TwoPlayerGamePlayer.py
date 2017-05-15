#basic super class for game players
#these are players who actually make moves in the game and (potentially) learn from the games
class TwoPlayerGamePlayer():
    #make a move as player @playerNumber in the game @game
    #often times this will also store some data about the game so that the function update works without any parameters.
    def makeMove(self, game, playerNumber):
        raise NotImplementedError
     
    #learn from the past game played. This is all   
    def update(self):
        raise NotImplementedError