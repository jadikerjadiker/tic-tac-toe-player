from TwoPlayerGame import TwoPlayerGame, IllegalMove

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
    def __init__(self, state = [[1, 1], [1, 1]]):
        TwoPlayerGame.__init__(self)
        self.state = state
        self.allStates = [self.state]
    
    def __str__(self):
        return str(self.state)
        
    def convertToStr():
        ans = ""
        for player in self.state:
            for hand in player:
                ans.append(str(hand))
        return ans
        
    def makeMove(self, move, playerNum):
        player = self.getPlayer(playerNum)
        if move==5:
            nonSplitHandNumber = None
            if player[0]==0:
                nonSplitHandNumber = 0
            elif player[1]==0:
                nonSplitHandNumber = 1
            
            otherHand = self.getHandOfPlayer(player, nonSplitHandNumber, other = True)
            
            #one of the hands is not 0 or the other hand is not even
            if nonSplitHandNumber==None or otherHand%2!=0:
                raise IllegalMove("Invalid attempt to split for player with position {}".format(player))
            
            #split it
            self.state[playerNum] = [otherHand//2]*2
        else:
            playerHandIndex = 1
            if move<3:
                playerHandIndex = 0
                
            otherPlayerHandIndex = 0
            if move%2==0:
                otherPlayerHandIndex = 1
                
            otherPlayer = self.getPlayer(playerNum, other = True)
            #actually do the move
            #make the opponent's hand the sum of the two hands and make it mod 5.
            otherPlayer[otherPlayerHandIndex] = (
                otherPlayer[otherPlayerHandIndex] + player[playerHandIndex])%5
            
                
    #returns a player (a list with two numbers), given the player number (1 or -1)
    #If other is True, it will return the other player
    def getPlayer(self, playerNum, other = False):
        if other:
            playerNum*=-1
        return self.state[self.playerNumberToIndex(playerNum)]
           
    #Converts a player number into the index at which to get the player from the game state
    #If other is True, it will use the player number of the other player
    #If given -1, it will return 0
    #If given 1, it will return 1
    def playerNumberToIndex(self, playerNum, other = False):
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
        

if __name__  == "__main__":
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
    