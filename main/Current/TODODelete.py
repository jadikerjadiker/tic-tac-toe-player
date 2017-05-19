if __name__ == "__main__":
    from TwoPlayerGameRunner import TwoPlayerGameRunner
    from ChopsticksGame import ChopsticksGame
    import UsefulThings as useful
    import Testers as test
    from ChopsticksOverAndOutGame import ChopsticksOverAndOutGame
    from TicTacToeGame import TicTacToeGame
    import pickle
    import numpy as np
    from scipy import stats
    from PPWithNNPlayer import PPWithNNPlayer
    
    #This tests the policy player
    policyPlayerInfo = {"exploreRate":0, "learningRate":.5, "rewards":[0, .7, 1], "defaultPolicyValue":.2}
    neuralNetInfo = {"architecture":[9, 9], "learningRate":.007}
    neuralNetTrainingInfo = {"mode":("specific", 0), "comment":1}
    examplesPerBatch = 10
    
    
    gameClass = TicTacToeGame
    gameRunner = TwoPlayerGameRunner(gameClass)
    gamesToPlay = 1000
    fileName = "trainSpecData.pkl"
    
    specRes = [] #[1st res1, 1st res2, ..., 2nd res1, ...]
    #for newPlayer in range(100):
    while True:
        p = PPWithNNPlayer(gameClass, policyPlayerInfo, neuralNetInfo, examplesPerBatch)
        for i in range(gamesToPlay):
            useful.printPercent(i, gamesToPlay, 5, 1)
            g = gameRunner.play(who = (p, 'random'))
            p.update()
        test.testAgainstRandom(p, gameClass, rounds = 10, gamesPerRound = 100, comment=2)