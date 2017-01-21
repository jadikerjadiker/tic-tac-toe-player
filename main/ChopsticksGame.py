from TwoPlayerGame import TwoPlayerGame, IllegalMove
from copy import deepcopy
from overrides import overrides
'''
The state of the game is represented by a list with four numbers. [[1, 2], [3, 4]]
The first two are player -1's left hand and right hand
...and the second two the player 1's left hand and right hand.

A move is specified by one number (and the player who makes the move)
The number 1 means the active player (the player making the move)
...uses their left hand (index 0) to hit their opponent's left hand (index 0):
1 is left hand to hit left hand (index 0 to index 0)
2 is left hand to hit right hand (index 0 to index 1)
3 is right hand to hit left hand (index 1 to index 0)
4 is right hand to hit right hand (index 1 to index 1)
5 is split

Splitting can only occur when one of the hands of a player is 0
...and the other hand is an even number.
Then, both hands of the player are set to be half the value
...of the non-0 hand

When a player hits an opponents hand, you add the two numbers together, mod 5
...(if more than 5 divide by 5 and get the remainder (i.e. %5)),
...and then that becomes the opponents hand.

If a hand is 0, it is out of the game.
When a player has both hands out of the game, they lose (and their opponent wins)

The game starts with a 1 on each hand for both players.
'''
class ChopsticksGame(TwoPlayerGame):
    def __init__(self, state = None):
        if state is None:
            state = [[1, 1], [1, 1]] #default
        TwoPlayerGame.__init__(self)
        self.state = state
        self.allStates = []
        self.saveState()
    
    def __str__(self):
        return str(self.state)
    
    #returns a player (a list with two numbers), given the player number (1 or -1)
    #If other is True, it will return the other player
    def getPlayer(self, playerNum, other = False):
        if other:
            playerNum*=-1
        return self.state[self.playerNumToIndex(playerNum)]
           
    #Converts a player number into the index at which to get the player from the game state
    #If other is True, it will use the player number of the other player
    #If given -1, it will return 0
    #If given 1, it will return 1
    def playerNumToIndex(self, playerNum, other = False):
        if other:
            playerNum*=-1
        return (playerNum+1)//2
    
    #given a player number and a hand number, returns the hand
    def getHand(self, playerNum, handNum, otherPlayer = False, otherHand = False):
        return self.getHandOfPlayer(self.getPlayer(playerNum, other = otherPlayer), handNum, other = otherHand)
    
    #given a player and a hand number, returns the hand of that player    
    def getHandOfPlayer(self, player, handNum, other = False):
        if other:
            handNum = self.getOtherIndex(handNum)
        return player[handNum]
            
    #Given the index of a player or the hand of a player,
    #...it will return the index of the other player or other hand of that same player
    #If given 0, it will return 1
    #If given 1, it will return 0
    def getOtherIndex(self, handIndex):
        return (handIndex+1)%2
        
    #Returns True if it is legal for this player to split, False otherwise
    #Can give it either a player or a playerNum
    #If given a playerNum, it will use that instead
    #In order to split, one of the hands needs to be zero, and the other needs
    #to be divisible by 2 (even)
    def canSplit(self, player = None, playerNum = None):
        if playerNum:
            player = self.getPlayer(playerNum)
        
        maxHand = max(player)
        if maxHand%2==0 and maxHand>0 and min(player)==0:
            return True
        else:
            return False

    @overrides
    def convertToStr(self):
        ans = ""
        for player in self.state:
            for hand in player:
                ans+=str(hand)
        return ans
    
    #Save the current state
    #(as a copy so it doesn't get edited by something editing the current state)    
    def saveState(self):
        self.allStates.append(deepcopy(self.state))
        
    @overrides
    def getPossibleMoves(self, playerNum):
        allMoves = {1:True, 2:True, 3:True, 4:True, 5:True}
        player = self.getPlayer(playerNum)
        otherPlayer = self.getPlayer(playerNum, other = True)
        if min #TODO finish
    
    @overrides
    def makeMove(self, move, playerNum):
        #makeMove() main
        player = self.getPlayer(playerNum)
        if move==5:
            #one of the hands is not 0 or the other hand is not even
            if not self.canSplit(player = player):
                raise IllegalMove("Invalid attempt to split for player with position {}".format(player))
            
            #split it
            #find the value of the non-largest hand and split it and set it to be the player
            self.state[self.playerNumToIndex(playerNum)] = [max(self.state[self.playerNumToIndex(playerNum)])//2]*2
        else:
            if move<0:
                raise IllegalMove("Invalid move '{}'".format(move))
            otherPlayer = self.getPlayer(playerNum, other = True)
            
            playerHandIndex = 1
            if move<3:
                playerHandIndex = 0
                
            otherPlayerHandIndex = 0
            if move%2==0:
                otherPlayerHandIndex = 1
            
            #if one of the hands is not in the game
            if player[playerHandIndex]==0 or otherPlayer[otherPlayerHandIndex]==0:
                raise IllegalMove("Invalid move '{}' for player '{}' with position {} against opponent with position {}".format(move, playerNum, player, otherPlayer))
                
            #actually do the move
            #make the opponent's hand the sum of the two hands and make it mod 5.
            otherPlayer[otherPlayerHandIndex] = (
                otherPlayer[otherPlayerHandIndex] + player[playerHandIndex])%5
        
        self.pastMoves.append((move, playerNum))       
        self.saveState() #add the new state to the list of all states

    @overrides
    #Undoes the last move of the game
    def undoMove(self):
        self.pastMoves.pop()
        self.allStates.pop()
        self.state = deepcopy(self.allStates[-1])
        
    
    @overrides
    #returns 1 if player 1 won, -1 if player -1 won, 0 if tie, and None if game is not complete
    def whoWon(self):
        for index, player in enumerate(self.state):
            #the player has only 0's (they are out of the game)
            if max(player)==0:
                return 
        
        
        
if __name__  == "__main__":
    from TwoPlayerGamePlayer import TwoPlayerGamePlayer
    gamePlayer = TwoPlayerGamePlayer(ChopsticksGame)
    while True:
        gamePlayer.play(who = ('random', 'human'))
    
    '''
    def moveAndPrint(game, move, player):
        game.makeMove(move, player)
        print(game)
    g = ChopsticksGame()
    print(g)
    moveAndPrint(g, 1, -1)
    moveAndPrint(g, 2, 1)
    moveAndPrint(g, 3, -1)
    moveAndPrint(g, 3, 1)
    moveAndPrint(g, 4, -1)
    moveAndPrint(g, 5, 1)
    #g.undoMove()
    print("g")
    print(g)
    print(g.pastMoves)
    h = g.getReversedPlayers()
    print(h)
    print(h.pastMoves)
    '''
    