'''
So the goal here is to have
*the policy player play a small amount of games
*the neural net learn to predict the policy based on the game position
*play the game based on the policy predicted by the neural net from the position

The TwoPlayerGame class will have to switch from using strings to using string representations of lists of numbers with consistent lengths.
Or, the games need to have a quick conversion between the strings for the PolicyPlayer and the consistent-lengthed lists for the neural net.

I decided to go with the "quick conversion between the strings for the PolicyPlayer and the consistent-lengthed lists for the neural net"
because it was easy for tic-tac-toe at least. Other games may need to implement their own complicated version.
'''

'''
So now we need to have the neural net train on the policy.
What is the structure of the policy?
'''

