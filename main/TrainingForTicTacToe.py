import NeuralNet
import TicTacToeGame as tttg
import random

'''
The goal of this is to create a neural network that will learn how to play tic-tac-toe.

Things to fool around with:
Training "away" from losing
How many games in each training batch
Net architecture
Training as random winner versus playing against random player

Things I could fool around with:
Regularization
Learning rate
'''
'''
Third strategy:
Have the neural net play against random nets and then learn from those games.
'''
class LearningNet3(NeuralNet.NeuralNet):
    def __init__(self, architecture, learningRate = 1, trainingMode = ('avg', .01), examplesPerBatch = 10):
        NeuralNet.NeuralNet.__init__(self, architecture, learningRate = learningRate, trainingMode = trainingMode)
        self.examplesPerBatch = examplesPerBatch #TODO see if this should be moved to NeuralNet
        self.version = 3.1
    
    '''
    Input: a list of finished two-player tic-tac-toe games or a single finished two-player tic-tac-toe game.
    Output:
    If there are only games with a winner, then the output is:
        a list of tuples [(game1State1, responseOfWinner), (game1State3, responseOfWinner), etc.]
    
    If there are only tie games, then the output is:
        a list of tuples [(game1State1, responseOfPlayer1), (game1State3, responseOfPlayer1), etc., (game1State2, responseOfPlayer2), (game1State4, responseOfPlayer2), etc.]
        
    And if there's both, then it will look something like:
        a list of tuples [(game1State1, responseOfWinner), etc., (game1State1, responseOfPlayer1), etc., (game1State2, responseOfPlayer2), etc.]
    
    gameState = [-1,-1, 0, 0, 0, 1, 0, 0, 1] where a -1 is the opponenent, and 1 is the winning player
    responseOfPlayer or responseOfWinner = [0, 0, 1, 0, 0, 0, 0, 0, 0], a one-hot vector/list where the 1 is where the winning player chose to move.
    (in this case, the player is going in the top right of the gameboard, blocking the opponenent's win, and winning down the right side)
    
    '''   
    def makeTrainingSet(self, gameList, examplesPerBatch = None):
        if examplesPerBatch==None:
            examplesPerBatch = -1
        ans = []
        batch = []
        batchCountdown = examplesPerBatch
        if not hasattr(gameList, "__iter__"):
            gameList = [gameList] #it used to be a single game, so now we're just making it into a list
        for game in gameList:
            winner = game.whoWon()
            assert winner!=None, "The game must be finished in order to make a training set out of it. Here is the game:\n{}".format(game)
            
            #make sure the winner is 1 so the game board doesn't have to be reversed when making the training examples
            if winner and winner==-1:
                game = game.getConvert()
                
            trainingGame = tttg.TicTacToeGame()
            #The computer is always considered to be 1 for the training sets
            #see if player 1 goes first
            myMove = (1==game.movesMade[0][1])
            for move in game.movesMade:
                #if we've added the right amount of games to the batch
                if batchCountdown==0:
                    ans.append(batch) #add the batch to the final training set
                    batch = [] #this actually reassigns batch to a new list, not overwriting the old one
                    batchCountdown = examplesPerBatch #reset the counter
                if myMove: #if player 1 is going
                    oneHotMove = [0]*9
                    oneHotMove[move[0]] = 1
                    batch.append(([boardSpace for boardSpace in trainingGame.board], oneHotMove))
                    batchCountdown-=1
                elif winner==0: #if the game's a tie, train for the other player as well
                    oneHotMove = [0]*9
                    oneHotMove[move[0]] = 1
                    #reverse the players on the board so it looks like it's player 1's turn
                    batch.append(([-boardSpace for boardSpace in trainingGame.board], oneHotMove))
                    batchCountdown-=1
                trainingGame.makeMove(*move)
                myMove = not myMove #next player's move
        if len(batch)>0:
            ans.append(batch)
        return ans
        
    #takes a game, the player number of this player and the player number of the opponent
    #returns the move this net makes as a number from 0 through 8
    def getMove(self, game, me = 1):
        #make sure I'm player 1 when I make the move
        if me==-1:
            myGame = game.getConvert()
        else:
            myGame = game
        responses = list(self.run(myGame.board))
        openSpaces = myGame.getOpenSpaces()
        assert len(openSpaces)>0, "The game must not be finished/full in order for the computer to make a move."
        topVal = -1 #default val because it's impossible (it's negative)
        ans = None
        for openSpace in openSpaces:
            if responses[openSpace]>topVal:
                topVal = responses[openSpace]
                ans = openSpace
        return ans
        
    def makeMove(self, game, player):
        game.makeMove(self.getMove(game, player), player)
    
    def go(self, gamesPerRound = 100, rounds = 5, comment = False, playAfterRound = False):
        games = []
        for roundNum in range(rounds):
            for gameNum in range(gamesPerRound):
                games.append(tttg.play(who = (self, 'random')))
            #for game in games:
            #    print(game)
            if comment>1:
                print("Training Round {}...".format(roundNum+1))
            trainingSet = self.makeTrainingSet(games, examplesPerBatch = self.examplesPerBatch)
            if comment>1:
                print("Training set completed. Testing to see how good I am at first.")
            firstResults = testAgainst(self, trainingSet, comment = comment)
            self.train(trainingSet, learningRate = self.learningRate, mode = self.trainingMode, comment = comment-1)
            if comment>1:
                print("Training complete!")
                print("Testing against training set again.")
            secondResults = testAgainst(self, trainingSet, comment = comment)
            if comment>1:
                improvement = [round(secondResults[i]-firstResults[i], 4) for i in range(len(firstResults))]
                print("Testing complete! Old results:\n{}\nNew results:\n{}\nThat's an improvement of\n{}".format(firstResults, secondResults, improvement))
            if comment>1:
                print("Training complete!")
                print("Testing against random players now.")
            testAgainstRandom(self, games = 1000, comment = comment-1)
            if playAfterRound:
                if askYesOrNo("Would you like to play against the net?"):
                    while True:
                        tttg.play(('human', self))
                        if not askYesOrNo("Would you like to play again?"):
                            break
        if comment>0:
            print("All training is complete!")
        if playAfterRound:
            print("You can just play now.")
            while True:
                tttg.play(('human', self))

'''
Fourth strategy:
Have the neural net play against itself.
Train itself to be more like the winner and less like the loser.
First it will play an entire game against itself.
Then, it will play a game alternating back and forth between itself and a random player
Then, it will play a game against a random player.
Right after each game, it will train itself to be more like the winner and less like the loser (or more like the tie)
'''
class LearningNet4(NeuralNet.NeuralNet):
    def __init__(self, architecture, learningRate = 1, trainingMode = ('avg', .01), examplesPerBatch = 10):
        NeuralNet.NeuralNet.__init__(self, architecture, learningRate = learningRate, trainingMode = trainingMode)
        self.examplesPerBatch = examplesPerBatch
        self.version = 4
    
    '''
    Input: a list of finished two-player tic-tac-toe games or a single finished two-player tic-tac-toe game.
    Output:
    If there are only games with a winner, then the output is:
        a list of tuples [(game1State1, responseOfWinner), (game1State3, responseOfWinner), etc.]
    
    If there are only tie games, then the output is:
        a list of tuples [(game1State1, responseOfPlayer1), (game1State3, responseOfPlayer1), etc., (game1State2, responseOfPlayer2), (game1State4, responseOfPlayer2), etc.]
        
    And if there's both, then it will look something like:
        a list of tuples [(game1State1, responseOfWinner), etc., (game1State1, responseOfPlayer1), etc., (game1State2, responseOfPlayer2), etc.]
    
    gameState = [-1,-1, 0, 0, 0, 1, 0, 0, 1] where a -1 is the opponenent, and 1 is the winning player
    responseOfPlayer or responseOfWinner = [0, 0, 1, 0, 0, 0, 0, 0, 0], a one-hot vector/list where the 1 is where the winning player chose to move.
    (in this case, the player is going in the top right of the gameboard, blocking the opponenent's win, and winning down the right side)
    
    '''   
    def makeTrainingSets(self, gameList, examplesPerBatch = None):
        if examplesPerBatch==None:
            examplesPerBatch = -1
        #the first list in ans is the one to hold the games it should train towards and the second list it should train away from.
        ans = ([], [])
        #batches and batchCountdowns are lists instead of tuples because they need to support assignment
        batches = [[], []]
        batchCountdowns = [examplesPerBatch, examplesPerBatch]
        if not hasattr(gameList, "__iter__"):
            gameList = [gameList] #it used to be a single game, so now we're just making it into a list
        for game in gameList:
            winner = game.whoWon()
            assert winner!=None, "The game must be finished in order to make a training set out of it. Here is the game:\n{}".format(game)
            
            #make sure the winner is 1 so the game board doesn't have to be reversed when making the training examples
            if winner and winner==-1:
                game = game.getConvert()
                
            trainingGame = tttg.TicTacToeGame()
            #The computer is always considered to be 1 for the training sets
            #see if player 1 goes first
            myMove = (1==game.movesMade[0][1])
            for move in game.movesMade:
                #dp
                print("Dealing with new move")
                print("batches before")
                print(batches)
                #if we've added the right amount of games to the batch
                for index, countdown in enumerate(batchCountdowns):
                    if countdown==0:
                        ans[index].append(batches[index]) #add the batch to the final training set
                        batches[index] = [] #this actually reassigns batch to a new list, not overwriting the old one
                        batchCountdowns[index] = examplesPerBatch #reset the counter
                print("batches middle")
                print(batches)
                if myMove: #if player 1 is going
                    oneHotMove = [0]*9
                    oneHotMove[move[0]] = 1
                    batches[0].append(([boardSpace for boardSpace in trainingGame.board], oneHotMove))
                    batchCountdowns[0]-=1
                else:
                    if winner==0: #if the game's a tie, train towards the other player
                        addTo = batches[0]
                        batchCountdowns[0]-=1
                    else: #if someone won, train away from the loser
                        addTo = batches[1]
                        batchCountdowns[1]-=1
                    oneHotMove = [0]*9
                    oneHotMove[move[0]] = 1
                    #reverse the players on the board so it looks like it's player 1's turn
                    addTo.append(([-boardSpace for boardSpace in trainingGame.board], oneHotMove))
                print("batches after")
                print(batches)
                trainingGame.makeMove(*move)
                myMove = not myMove #next player's move
        #dps
        print("batches")
        print(batches)
        for index, batch in enumerate(batches):
            if len(batch)>0:
                ans[index].append(batch)
        return ans
        
    #takes a game, the player number of this player and the player number of the opponent
    #returns the move this net makes as a number 0 through 8
    def getMove(self, game, me = 1):
        #make sure I'm player 1 when I make the move
        if me==-1:
            myGame = game.getConvert()
        else:
            myGame = game
        responses = list(self.run(myGame.board))
        openSpaces = myGame.getOpenSpaces()
        assert len(openSpaces)>0, "The game must not be finished/full in order for the computer to make a move."
        topVal = -1 #default val because it's impossible (it's negative)
        ans = None
        for openSpace in openSpaces:
            if responses[openSpace]>topVal:
                topVal = responses[openSpace]
                ans = openSpace
        return ans
        
    def makeMove(self, game, player):
        game.makeMove(self.getMove(game, player), player)
    
    def go(self, gamesPerRound = 100, rounds = 5, comment = False, playAfterRound = False):
        games = []
        for roundNum in range(rounds):
            for gameNum in range(gamesPerRound):
                games.append(tttg.play(who = (self, 'random')))
            #for game in games:
            #    print(game)
            if comment>1:
                print("Training Round {}...".format(roundNum+1))
            self.train(self.makeTrainingSet(games, examplesPerBatch = self.examplesPerBatch), learningRate = self.learningRate, mode = self.trainingMode, comment = comment-1)
            if comment>1:
                print("Training complete!")
                print("Testing against random nets.")
            testAgainstRandom(self, games = 1000, comment = comment)
            #TODO add in "Sorry, I couldn't understand that" type stuff
            if playAfterRound:
                if askYesOrNo("Would you like to play against the net?"):
                    while True:
                        tttg.play(('human', net))
                        if not askYesOrNo("Would you like to play again?"):
                            break
        if comment>0:
            print("All training is complete!")
        if playAfterRound:
            print("You can just play now.")
            while True:
                tttg.play(('human', 'human'))

def askYesOrNo(question):
    while True:
        try:
            ans = raw_input(question+" (y/n) ").lower()
            if ans in ['y', 'yes', 'yeah', 'yep']:
                return True
            elif ans in ['n', 'no', 'nope']:
                return False
            else:
                raise RuntimeError("Bad input")
        except:
            print("Answer was not 'y' or 'n'.")

def testAgainst(net, batches, comment = False):
    if comment>0:
        print("Started testing net against pre-made batches.")
    batchesLen = len(batches)
    results = [0]*batchesLen #will end up being [percentCorrectOnBatch1, percentCorrectOnBatch2, ...]
    for batchNum, batch in enumerate(batches):
        batchLen = len(batch)
        if comment>1:
            print("Testing batch {}/{}".format((batchNum+1), batchesLen))
        for exampleNum, example in enumerate(batch):
            if comment>2:
                print("Testing example {}/{}".format((exampleNum+1), batchLen))
            fakeGame = tttg.TicTacToeGame()
            fakeGame.board = example[0]
            if example[1][net.getMove(fakeGame)]==1:
                results[batchNum]+=1
        
        results[batchNum]=round(results[batchNum]*1.0/len(batch), 4) #average the result and round it
        if comment>2:
            print("Results so far: {}".format(results[:batchNum+1]))
    if comment>0:
        print("Final result of testing net against pre-made batches: {}".format(results))
    return results

def testAgainstRandom(net, games = 100, comment = False):
    results = [0]*3 #[losses, ties, wins] for the net
    for gameNum in range(games):
        if comment>1:
            print("Testing game {}/{}".format((gameNum+1), games))
        game = tttg.TicTacToeGame()
        player = random.choice([1, -1])
        while game.whoWon()==None:
            if player==1:
                net.makeMove(game, 1)
            else: #player==-1
                tttg.makeRandomMove(game, -1)
            player*=-1
            
        results[game.whoWon()+1]+=1
        if comment>1:
            if comment>2:
                print(game)
            print("Results so far:\n{}".format(results))
    if comment>0:
        print("Final results:\n{}".format(results))
    return results
            
                
  
if __name__ == '__main__':
    '''
    game = tttg.makeRandomGame()
    while (not game.whoWon()) or (len(game.movesMade)>6):
        game = tttg.makeRandomGame()
    net = LearningNet4([9, 9, 9, 9])
    print(game)
    print(net.makeTrainingSets(game))
    '''
    '''
    net = LearningNet3([9, 9, 9, 9], learningRate = .1, trainingMode = ('avgAvg', .15), examplesPerBatch = 20)
    net.go(gamesPerRound = 500, rounds = 100)
    '''
    '''
    net = LearningNet3([9, 9, 9, 9], learningRate = .01, trainingMode = ('avgAvg', .01))
    #game = tttg.playHumanVRandom()
    trainingSet = []
    for i in range(100):
        trainingSet.append(tttg.makeRandomGame())
    trainingSet = net.makeTrainingSet(trainingSet)
    print(trainingSet)
    print("Training started")
    net.train(trainingSet, comment = True)
    print("Training ended")
    '''

    #Testing range of error for playing against random nets
    '''
    TODO
    The training shouldn't be making it do worse on its own training set/batch
    So, either how I'm evaluating how well it's doing is off, or how I'm training it is off.
    Also, it's very odd that with this set up, the second improvement list is always "0".
    Why doesn't it do any training on that second round? (Does it do training and something's just not working?)
    '''
    net = LearningNet3([9, 9, 9, 9], learningRate = .01, trainingMode = ('avg', .19), examplesPerBatch = 300)
    net.go(gamesPerRound = 500, rounds = 2, comment = 2)
    testRuns = 50
    gamesPerTest = 1000
    lows = [gamesPerTest+1]*3
    highs = [-1]*3
    overall = [0]*3
    for i in range(testRuns):
        test = testAgainstRandom(net, games = gamesPerTest)
        for j, testVal in enumerate(test):
            lows[j] = min(lows[j], testVal)
            highs[j] = max(highs[j], testVal)
            overall[j]+=testVal
        print(test)
    ranges = [highs[i]-lows[i] for i in range(3)]
    print("Lows: {}".format(lows))
    print("Highs: {}".format(highs))
    print("Ranges: {}".format(ranges))
    avgs = [overall[i]*1.0/testRuns for i in range(3)] #the *1.0 makes it so it doesn't use integer division 
    print("Averages: {}".format(avgs))
    
    '''
    #Training workhorse
    response = [0]*9
    for i in range(100):
        sky = LearningNet1([9, 9, 9, 9, 9], trainingGameAmt = 1000, learningRate = 1, trainingMode = ('error', .01))
        sky.go(comment = False)
        game = tttg.TicTacToeGame()
        response[sky.getMove(game, 1, -1)]+=1
        print("RESPONSE {}: {}".format(i+1, response))
    print(response)
    '''
        