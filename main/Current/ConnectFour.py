from PPWithNNTwoPlayerGame import PPWithNNTwoPlayerGame

class ConnectFour(PPWithNNTwoPlayerGame):
    #inputLen outputLen and allMoves are set in init
    #TODO these should be instance properties because I may want to change them based on how the class is inited
    inputLen = None
    outputLen = None
    allMoves = [0, 1, 2, 3, 4, 5, 6, 7]