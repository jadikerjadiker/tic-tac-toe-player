import TicTacToeGame as tttg
import random
import UsefulThings as useful

def testAgainstRandom(player, rounds = 50, gamesPerTest = 1000, comment = 1, pctIncrement = 2):
    def oneRound(player, games, comment):
        results = [0]*3 #[losses, ties, wins] for the player
        for gameNum in range(games):
            if comment>1:
                print("Testing game {}/{}".format((gameNum+1), games))
            game = tttg.TicTacToeGame()
            playerNum = random.choice([1, -1])
            while game.whoWon()==None:
                if playerNum==1:
                    player.makeMove(game, 1)
                else: #player==-1
                    tttg.makeRandomMove(game, -1)
                playerNum*=-1
                
            results[game.whoWon()+1]+=1
            if comment>1:
                if comment>2:
                    print(game)
                print("Results so far in round:\n{}".format(results))
        if comment>0:
            print("Results of one round:\n{}".format(results))
        return results
        
    lows = [gamesPerTest+1]*3
    highs = [-1]*3
    overall = [0]*3
    for i in range(rounds):
        test = oneRound(player, games = gamesPerTest, comment = comment-1)
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