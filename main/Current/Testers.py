import random
import UsefulThings as useful

def testAgainstRandom(player, game, rounds = 50, gamesPerRound = 1000, gameParameters = None, comment = 1, pctIncrement = 2):
    def oneRound(player, gameClass, numberOfGames, gameParameters, comment):
        results = [0]*3 #[losses, ties, wins] for the player
        for gameNum in range(numberOfGames):
            if comment>1:
                print("Testing game {}/{}".format((gameNum+1), numberOfGames))
            game = gameClass(*gameParameters[0], **gameParameters[1])
            playerNum = random.choice([0, 1])
            while game.whoWon()==None:
                if playerNum==0:
                    player.makeMove(game, 0)
                else: #player==1
                    game.makeRandomMove(1)
                playerNum = game.getOtherPlayerNum(playerNum)
            
            #convert the whoWon() value (-1 for tie, 0 for test player win, 1 for test player loss)
            #into an index for the list [loss, tie, win]
            #then increase the value at that index by 1.
            results[(game.whoWon()+2)%3]+=1
            if comment>1:
                if comment>2:
                    print(game)
                print("Results so far in round:\n{}".format(results))
        if comment>0:
            print("Results of one round:\n{}".format(results))
        return results
    
    #testAgainstRandom() main
    if gameParameters is None:
        gameParameters = ([], {})
    lows = [gamesPerRound+1]*3
    highs = [-1]*3
    overall = [0]*3
    for i in range(rounds):
        test = oneRound(player = player, gameClass = game, numberOfGames = gamesPerRound, gameParameters = gameParameters, comment = comment-1)
        if pctIncrement>0:
            useful.printPercent(i, rounds, incrementAmt = pctIncrement)
        for j, testVal in enumerate(test):
            lows[j] = min(lows[j], testVal)
            highs[j] = max(highs[j], testVal)
            overall[j]+=testVal
    ranges = [highs[i]-lows[i] for i in range(3)]
    print("Lows: {}".format(lows))
    print("Highs: {}".format(highs))
    print("Ranges: {}".format(ranges))
    avgs = [overall[i]*1.0/rounds for i in range(3)] #the *1.0 makes it so it doesn't use integer division 
    print("Averages: {}".format(avgs))
    return (lows, highs, ranges, avgs)