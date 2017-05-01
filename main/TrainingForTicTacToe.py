import NeuralNet
import TicTacToeGame as tttg
import random
import LogicalPlayer as lp
import UsefulThings as useful

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
        self.examplesPerBatch = examplesPerBatch
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
            examplesPerBatch = self.examplesPerBatch #use the default
        if examplesPerBatch==None:
            examplesPerBatch = -1 #if even the default is None, that should be converted to -1
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
                games.append(tttg.play(who = ('random', 'random')))
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
                print("Testing complete! Old results:\n{}\nNew results:\n{}\nThat's an improvement of\n{}\nAnd an overall improvement of\n{}".format(firstResults, secondResults, improvement, sum(improvement)))
            if comment>1:
                print("Training complete!")
                print("Testing against random players now.")
            if playAfterRound:
                if useful.askYesOrNo("Would you like to play against the net?"):
                    while True:
                        tttg.play(('human', self))
                        if not useful.askYesOrNo("Would you like to play again?"):
                            break
        if comment>0:
            print("All training is complete!")
        if playAfterRound:
            print("You can just play now.")
            while True:
                tttg.play(('human', self))

'''
Fourth strategy:
Have the neural net play against a semi-good opponent.

It will train itself towards the winner and away from the loser
'''
class LearningNet4(NeuralNet.NeuralNet):
    def __init__(self, architecture, learningRate = 1, trainingMode = ('avg', .01), examplesPerBatch = None):
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
    def makeTrainingSets(self, gameList):
        #cache (store it so we don't have to keep on accessing the property; it's just a local variable)
        if self.examplesPerBatch==None:
            examplesPerBatch = -1 #if even the default is None, that should be converted to -1
        else:
            examplesPerBatch = self.examplesPerBatch
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
                #if we've added the right amount of games to the batch
                for index, countdown in enumerate(batchCountdowns):
                    if countdown==0:
                        ans[index].append(batches[index]) #add the batch to the final training set
                        batches[index] = [] #this actually reassigns batch to a new list, not overwriting the old one
                        batchCountdowns[index] = examplesPerBatch #reset the counter
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
                trainingGame.makeMove(*move)
                myMove = not myMove #next player's move
    
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
                game = tttg.play(who = (self, lp.LogicalPlayer()))
                games.append(game)
                #print(game) #can be commented out when not wanted
            if comment>1:
                print("Training Round {}...".format(roundNum+1))
            trainingSet = self.makeTrainingSets(games)
            if comment>1:
                print("Training set completed. Testing to see how good I am at first.")
            firstResults = testAgainst(self, trainingSet[0], comment = comment)
            self.trainBoth(trainingSet, learningRate = self.learningRate, mode = self.trainingMode, comment = comment-1)
            if comment>1:
                print("Training complete!")
                print("Testing against training set again.")
            secondResults = testAgainst(self, trainingSet[0], comment = comment)
            if comment>0:
                improvement = [round(secondResults[i]-firstResults[i], 4) for i in range(len(firstResults))]
                print("Testing complete! Old results:\n{}\nNew results:\n{}\nThat's an improvement of\n{}\nAnd an overall improvement of\n{}".format(firstResults, secondResults, improvement, sum(improvement)))
            if comment>1:
                print("Training complete!")
            if playAfterRound:
                if useful.askYesOrNo("Would you like to play against the net?"):
                    while True:
                        tttg.play(('human', net))
                        if not useful.askYesOrNo("Would you like to play again?"):
                            break
        if comment>0:
            print("All training is complete!")
        if playAfterRound:
            print("You can just play now.")
            while True:
                tttg.play(('human', 'human'))

'''
5th strategy:
Have the neural net learn from logical player v logical player games.
'''
class LearningNet5(NeuralNet.NeuralNet):
    def __init__(self, architecture, learningRate = 1, trainingMode = ('avg', .01), examplesPerBatch = 10):
        NeuralNet.NeuralNet.__init__(self, architecture, learningRate = learningRate, trainingMode = trainingMode)
        self.examplesPerBatch = examplesPerBatch
        self.version = 5
    
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
            examplesPerBatch = self.examplesPerBatch #use the default
        if examplesPerBatch==None:
            examplesPerBatch = -1 #if even the default is None, that should be converted to -1
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
                games.append(tttg.play(who = (LogicalPlayer.LogicalPlayer(), lp.LogicalPlayer())))
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
            if comment>0:
                improvement = [round(secondResults[i]-firstResults[i], 4) for i in range(len(firstResults))]
                print("Testing complete! Old results:\n{}\nNew results:\n{}\nThat's an improvement of\n{}\nAnd an overall improvement of\n{}".format(firstResults, secondResults, improvement, sum(improvement)))
            if comment>1:
                print("Training complete!")
            if playAfterRound:
                if useful.askYesOrNo("Would you like to play against the net?"):
                    while True:
                        tttg.play(('human', self))
                        if not useful.askYesOrNo("Would you like to play again?"):
                            break
        if comment>0:
            print("All training is complete!")
        if playAfterRound:
            print("You can just play now.")
            while True:
                tttg.play(('human', self))

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
                game.makeRandomMove(-1)
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
    #This was interesting in many ways:
    #1: after the 3rd round, it basically just stopped responding to training, then seemed to break out of it's non-response
    #I attribute that to it being stuck in a really small valley that it took a long time to get out of
    #2: It seemed to try to pull off complicated forks, but stick to it regardless of the opponent's moves.
    net = LearningNet4([9, 9, 9, 9], learningRate = .002, trainingMode = ('iter', 10), examplesPerBatch = 1000)
    #def go(self, gamesPerRound = 100, rounds = 5, comment = False, playAfterRound = False):
    net.go(gamesPerRound = 1000, rounds = 1000, comment = 4, playAfterRound = True)
    '''
    net = LearningNet3([9, 9, 9, 9], learningRate = .002, trainingMode = ('iter', 10), examplesPerBatch = None)
    #def go(self, gamesPerRound = 100, rounds = 5, comment = False, playAfterRound = False):
    net.go(gamesPerRound = 1000, rounds = 5, comment = 3, playAfterRound = True)
    '''
    '''
    #Play against human
    net = LearningNet3([9, 9, 9, 9], learningRate = .01, trainingMode = ('iter', 100), examplesPerBatch = None)
    gameList = []
    while True:
        game = tttg.play(who = ('human', net))
        gameList.append(game)
        net.train(net.makeTrainingSet(gameList), comment = 3)
    '''
    '''
    The goal of this is to test why it is that I can train on a batch and get worse results than being random.
    '''
    '''
    print("running")
    found = []
    for i in range(100):
        gameList = []
        while len(gameList)<100:
            game = tttg.TicTacToeGame.makeRandomGame()
            #while len(game.movesMade)!=5:
                #game = tttg.TicTacToeGame.makeRandomGame()
            gameList.append(game)
            #print(game)
        net = LearningNet3([9, 30, 9], learningRate = .001, trainingMode = ('avg', .054), examplesPerBatch = None)
        trainingSet = net.makeTrainingSet(gameList)
        old = testAgainst(net, trainingSet, comment = False)
        net.train(trainingSet, comment = 3)
        new = testAgainst(net, trainingSet, comment = False)
        improvement = [round(new[i]-old[i], 4) for i in range(len(old))]
        #print(old)
        #print(new)
        print(improvement)
        if improvement[0]<0:
            print("FOUND ONE!!!")
            found.append(improvement[0])
        print("Found so far: {}".format(found))
    print("Done!")
    print("Found {}".format(len(found)))
    print(found)
    #there are still some nets doing worse, even though the training seems to be working perfecly. It just doesn't make sense.
    '''
    '''
    net = LearningNet3([9, 9, 9, 9], learningRate = .1, trainingMode = ('avgAvg', .15), examplesPerBatch = 300)
    net.go(gamesPerRound = 500, rounds = 1, comment = 2)
    '''
    '''
    game = tttg.TicTacToeGame.makeRandomGame()
    while (not game.whoWon()) or (len(game.movesMade)>6):
        game = tttg.TicTacToeGame.makeRandomGame()
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
        trainingSet.append(tttg.TicTacToeGame.makeRandomGame())
    trainingSet = net.makeTrainingSet(trainingSet)
    print(trainingSet)
    print("Training started")
    net.train(trainingSet, comment = True)
    print("Training ended")
    '''

    #Testing range of error for playing against random nets
    '''
    The training shouldn't be making it do worse on its own training set/batch
    So, either how I'm evaluating how well it's doing is off, or how I'm training it is off.
    Also, it's very odd that with this set up, the second improvement list is always "0".
    Why doesn't it do any training on that second round? (Does it do training and something's just not working?)
    
    So the issue with this is that if the avgAvg just jumps around, it's not really learning all that well and will just do worse.
    The learningRate needs to be small enough so that the net actually learns, not just jumps around until it hits a valley
    '''
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
        