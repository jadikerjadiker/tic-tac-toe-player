from TwoPlayerGame import TwoPlayerGame, IllegalMove
from copy import deepcopy
'''
The state of the game is represented by a list with four numbers. [[1, 2], [3, 4]]
The first two are player -1's left hand and right hand
...and the second two the player 1's left hand and right hand.

A move is specified by one number (and the player who makes the move)
The number 1 means the active player (the player making the move)
...uses their left hand to hit their opponent's left hand.
1 is left hand to hit left hand
2 is left hand to hit right hand
3 is right hand to hit left hand
4 is right hand to hit right hand
5 is split

Splitting can only occur when one of the hands is 0
...and the other hand is an even number.
Then, both hands of the player are set to be half the value
...of the non-0 hand
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
        
    def convertToStr():
        ans = ""
        for player in self.state:
            for hand in player:
                ans.append(str(hand))
        return ans
    
    #Save the current state
    #(as a copy so it doesn't get edited by something editing the current state)    
    def saveState(self):
        self.allStates.append(deepcopy(self.state))
        
    def makeMove(self, move, playerNum):
        #returns a player (a list with two numbers), given the player number (1 or -1)
        #If other is True, it will return the other player
        def getPlayer(playerNum, other = False):
            if other:
                playerNum*=-1
            return self.state[playerNumToIndex(playerNum)]
               
        #Converts a player number into the index at which to get the player from the game state
        #If other is True, it will use the player number of the other player
        #If given -1, it will return 0
        #If given 1, it will return 1
        def playerNumToIndex(playerNum, other = False):
            if other:
                playerNum*=-1
            return (playerNum+1)//2
        
        #given a player number and a hand number, returns the hand
        def getHand(playerNum, handNum, otherPlayer = False, otherHand = False):
            return getHandOfPlayer(getPlayer(playerNum, other = otherPlayer), handNum, other = otherHand)
        
        #given a player and a hand number, returns the hand of that player    
        def getHandOfPlayer(player, handNum, other = False):
            if other:
                handNum = getOtherIndex(handNum)
            return player[handNum]
                
        #Given the index of a player or the hand of a player,
        #...it will return the index of the other player or other hand of that same player
        #If given 0, it will return 1
        #If given 1, it will return 0
        def getOtherIndex(handIndex):
            return (handIndex+1)%2
        
        #makeMove() main
        player = getPlayer(playerNum)
        if move==5:
            nonSplitHandNumber = None
            if player[0]==0:
                nonSplitHandNumber = 0
            elif player[1]==0:
                nonSplitHandNumber = 1
            
            otherHand = getHandOfPlayer(player, nonSplitHandNumber, other = True)
            
            #one of the hands is not 0 or the other hand is not even
            if nonSplitHandNumber==None or otherHand%2!=0:
                raise IllegalMove("Invalid attempt to split for player with position {}".format(player))
            
            #split it
            self.state[playerNumToIndex(playerNum)] = [otherHand//2]*2
        else:
            playerHandIndex = 1
            if move<3:
                playerHandIndex = 0
                
            otherPlayerHandIndex = 0
            if move%2==0:
                otherPlayerHandIndex = 1
                
            otherPlayer = getPlayer(playerNum, other = True)
            #actually do the move
            #make the opponent's hand the sum of the two hands and make it mod 5.
            otherPlayer[otherPlayerHandIndex] = (
                otherPlayer[otherPlayerHandIndex] + player[playerHandIndex])%5
        
        self.pastMoves.append((move, playerNum))       
        self.saveState() #add the new state to the list of all states

    #Undoes the last move of the game
    def undoMove(self):
        self.pastMoves.pop()
        self.allStates.pop()
        self.state = deepcopy(self.allStates[-1])
        
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
    