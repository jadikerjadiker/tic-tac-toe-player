from Game import *

if __name__ == "__main__":
    g = makeRandomGame()
    while not ((0 in g.board) and g.whoWon()==0):
        g = makeRandomGame()
    
    print(g)
    print(g.whoWon())
        