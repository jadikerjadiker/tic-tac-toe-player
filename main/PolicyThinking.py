'''
Okay, so architecture of this thing

Main one is a list with a list inside
[[initial game for player 1, [games that result from this]], [initial game for player2, [games that result from this]]]
where
[games that result from this] = [[game1, [games that result from game 1]], [game2, [games that result from game 2]], ...]

Then, we can tell where we are by tracking the indexes
[0, 1, 3] would mean policy[0][1][1][1][3]

What if instead, it were
Main one is a list with a list inside
[initial game for player 1, [games that result from this], initial game for player2, [games that result from this]]
where
[games that result from this] = [game1, [games that result from game 1], game2, [games that result from game 2], ...]
Then, we can tell where we are by tracking the indexes
[0, 2, 6] would mean policy[0+1][2+1][6]
#all the indexes for the actual game would be even, and that game's branches would be odd.

I think the latter one is easier for me to understand, so I'm going to go with that. Less nesting.

Wait, what if we did linked lists?
l1 = [initial game for player 1, initial game for player 2]
l2 = [[games that result from initial player 1 game], [games that result from initial player 2 game]]
where
games that result from initial player 1 game = [g1.1, g1.2, g1.3, ...]
l3 = [[[g1.1.1, g1.1.2, ...], [g1.2.1, g1.2.2, ...], ...], [[g2.1.1, g2.1.2, g2.1.3, ...], [g2.2.1, g2.2.2, ...], ...], ...]

so policy = [l1, l2, l3]

Then, we can tell what policy we should use by tracking the indexes/moves made
myPolicyTracked = [1, 3, 5] #this would be a player going second who made move 3 and then move 5
myPolicy = policy[len(myPolicy)-1][1][3][5] which is really quite simple

I think I'll use this version.

Another thing I can do with this one is replace the lists with dictionaries.
That way I don't have to create new policies I'm not using and keep track of the order of them.
policy will be a dictionary of dictionaries then.
'''

'''
So I started programming the policy player as mentioned in the last comment section, only to realize that there isn't just
...one starting game for going second; there are 9.
So, what if each l0, l1, l2, etc was a move. l0 is full of games with 0 moves taken, l1, with games with 1 move taken.

The issue with this is that I can't just easily update a player for a win.

#note that the moves are in computer numbers, so 4 is the middle and 0 is the upper left

For example, myPolicyTracked = [0, 4, 1, 8, 2] #first player winning on the top line
would require it to update policy[4][0][4][1][8][2], policy[2][0][4][1], and policy[0][0] if only updating the winner
and myPolicyTracked = [2, 4, 1, 0, 5, 8] #second player wins with diagnol to bottom-right
would require it to update policy[5][2][4][1][0][5][8], policy[3][2][4][1][0], and policy[1][2][4].

Overall, what I'm trying to say is that it's almost always complicated to only update one side of things.
If I had it play against itself, it would "learn weaknesses in itself" and update,
...playing against greedy version of self might be the best option.
And then it would be easier to just update both sides.

But, is this whole index madness really the best way to go?

This doesn't even track which player is going, does it?
Actually it does; [2,4] is different than [4,2] by quite a bit.
Its always assumed that the policy player should be making the move at that particular policy
which implies that it is the one who is currently occupying space 2 in the [2,4] example.

So I think that this architecture is actually alright. The only thing that bothers me is that I feel like that first index can go.
The first index is just dependant on how many follow. Is there any way to make it not?

I think that would require a policy to be subscriptable, which I don't want to deal with, though it would make things easier.
Hmm. Maybe I should program that, learn a little more about Python.

Here, in case I'm just not thinking as clearly later on, the reason why I can't do it without a subscriptable policy is because
...if I have policy[0] representing a policy where someone has gone in the top left corner,
...and policy[0][4] represent a policy where someone has gone in the top left and middle,
...then that original policy must be subscriptable

So maybe I need each policy to have subpolicies.
And then the player determines moves from just a single policy of an empty board with tons of subpolicies.
Interesting. I like it. It will make me learn more Python.
'''

'''
Beyond the architecture, there are many different ways to train, just like the nets.
I really like the idea of it playing against itself.
I feel like that will be the best way for it to learn its weaknesses.

The reason why this isn't perfect is because if it plays itself to a tie, it could stagnate.
But, unless that is perfect play, one of them should explore, which will shift everything.
So in other words, they both can't always be greedy, which makes sense.

So, there are different variables:
How well trained is each net?
How greedy is each net?
What is the learning rate for each net?
How many games do the nets play?
How does the learning rate decrease as they play? Linearly?

If I just have the net play its (current) self for each training, I fear it will learn slowly and tie itself often.
But at the same time, it would be kinda cool.

I think it would be better to have a pretty non-greedy net play a pretty greedy net.
That way we get the best of both worlds.

The question is how to combine it into one policy.

Playing against a random player just seems like a really bad idea because
...it will just exploit the stupidity of the random player and thus learn bad moves.

So I definitely want it to play against some version of "itself"

Another option is to have it play against its (greedy) past self for like 100 games,
...and then do that over and over.

Actually, instead of having it play against its current self with both sides exploring sometimes
...(because then both their exploring would be based on potentially their sub-optimal play)
...the policy should be fairly non-greedy, and then play against a completely greedy version of itself for x games.

If 1, then it is playing itself, but without the chance of learning weaknesses in its own unverified weakness.
It will only learn the weaknesses in its own percieved strengths.
And then there's no "combining" the two policies. It just updates as it plays and switches out its opponent after so many games.

But, this should not be its only way of training, it should be a particular mode of training.

Oh wait, but what if it doesn't know what it's doing in a certain part? How does the static greedy player with no info react? Just random?
How can the "real" policy learn from its static copy?

Maybe it is best to average them. But that would take so much time.
Maybe it has to keep track of where it explored new territory, and then theres a combination function that combines what the two learned.
If one player is always going first (which is the case when they only play one game before combining),
...the combination function is actually fairly simple: just replace the unknowns with the new policies or add the new policies into the dicts.
Since there was nothing there before, you should just be able to add them in;
...it won't have any data on it because it's learning from the other player's side.

But if there's more than one game going on, then things get tricky because you can either average them,
...or just take them from one player's side, or other options.
For now, I think I'll just stick with the "play one game against a greedy version of yourself, and if the greedy version has to go someplace new during the game, incorporate it into yourself."
'''