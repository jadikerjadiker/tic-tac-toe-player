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
For now, I think I'll just stick with the
..."play one game against a greedy version of yourself, and if the greedy version has to go someplace new during the game, incorporate it into yourself."
Note that "going someplace new" is not exploring. Even a completely greedy player can be put in a new position on which it has no info
'''

'''
So I've reread the Sutton version (http://webdocs.cs.ualberta.ca/~sutton/book/ebook/), and it doesn't seem all that smart.
In his version, it appears that if you make a greedy move, then an exploratory move, the initial position's value moves closer to the position after the greedy move,
...even though the greedy move wasn't updated with any new data. I think that's ridiculous. I shouldn't be reinforcing choices with no new data.

What that's telling the computer is "If this position is good, then it's a solid choice if I keep on exploring, if it's bad, it's a terrible choice if I keep on exploring."
How good a spot is should have nothing to do with exploring. It should have to do with whether or not you win if you play your best from that position.

What good does two explorations in a row do in Sutton's? You would have learned more if you just did 1.

So, I think for mine, I want it to only update the stuff that happens after the first exploration.
And, in addition, the policy player should only explore once in a given game.
Will that cut down on my chances of finding good combos?
I honestly don't know. But I also don't understand how exploring twice would help me to exploit the combo.
Maybe it's because then if I won it would become the greedy option on that new exploration the next time.
That makes sense.

So I guess I'm okay with exploring more than once.
Another reason why I like that is because it's really hard to figure out what a good exploration rate would be
...if you can only explore once. Does it increase over each game so the more moves the more likely, or what?

So yeah, I'm deviating slightly from Sutton by only updating up to the last exploring move.

Sutton also seems to be saying that we should be updating after every move,
...whereas the student's paper's progam appears to only update after the entire game is complete.
I like updating only after the game is complete. It makes sense that the first move, not just the second to last move,
...should be given credit for a win
'''

'''
Given these choices I've made, what are the things the computer needs to know to update its policies?

1. The moves taken by at least one player and the value of the final state for that player (the "reward")
2. The last exploratory move made by that player.

To make things easier, let's make a method that just updates based on its last play, given how the game turned out.
Then, all I need to know is the trace from the last move the computer made and the game
But it seems silly to rely on something like that in case I want to change it later.
I'd much rather just pass it the game and its number and make it learn from that.
That way, it's more modifiable.

But, I also need the last exploratory move.
I think the easiest way to do that is to have a list of all the exploratory moves in the game.
(That way, if I use this function to update from the other player, their exploratory moves are already in the list.
...And it also helps if I decide to do more updating (like, before an exploratory move) later on)

So then how does the PolicyPlayer know what moves were exploratory or not?
Maybe it keeps track in its own property of the exploratory moves it made in the last game?
But the makeMove function just takes a game with no indication as to whether or not it is new.
So it won't know if it's getting a new game or an old game.

But this update function could clear a property with a list of exploratory moves once it's done using them.
And the class can tell if it's a new game (just not a partial game to a partial game)

I like the update function just using whatever is on the list.
It's a little wild because there's no real way to control what's on the list (what happens if it doesn't update after every game?)

I think having the makeMove function deal with checking to see if it's a new game will work out best.
I can't imagine having a situation in which we have the policy player play on and train from an already played board.
But, the parameter to the training function should allow a list of exploratory moves just in case something like that does happen.
(It will just default to be the player's property)
'''

'''
As I began thinking about transitioning over to Chopsticks (now that I've gotten results like an average of 1.56 losses out of 1000 games)
I realized that Chopsticks has to keep track of if it's in a repeat position.
In other words, the policies depend on the board state, not just the moves that got it there.
Then, I realized that tic-tac-toe is the same way.
The move sequence (in human numbers) (3, 9, 1) should not differ from (1, 9, 3),
...yet to the policy player I currently have, they're completely different positions.
So it may make it much more efficient.
What I want to calculate is how many fewer positions the player will have to learn.
The old one counted each move separately, and so had (at most) 9! = 362880 positions to learn
The one I will make that just looks at the board will have (at most) 3^9 = 19683 positions to learn.
(The "at most" is there because non-tie positions will end before the entire board is filled, eliminating many impossible positions)

Thats about 18 times fewer positions to learn. 343,197 fewer positions, to be exact.
I think adding in the board functionality would be a "game changer" :)
'''

'''
So, it's a weird way of doing it, but I totally could just index the policy 9 times.
The first index is 0, 1, or 2 depending on who's in position 0, etc.

Nah, that's just weird. I'm better off having a table of who is where, where -1 is opponent and 1 is self.

So the moves in spots (3, 9, 1), if the policy player went first, would be [0, 0, 1, 0, 0, 0, 0, 0, 0], etc.
You know what? That looks like a one-hot. Let's just use dictionaries. So it becomes a dict like
(switching over to computer numbers, so the moves are now (2, 8, 0))
{2:1}, {2:1, 8:-1}, {0:1, 2:1, 8:-1}
But that also makes it so that if I have a trace, I can't just get the dict. Wait, can I?
Is there a way to index something with a dictionary?
Not that I can find.

The best method right now is seeming to be converting the game into a string or a number.
Probably a string, but to the game I don't think it really matters.

So I guess converting the game to a string is the best method right now.
It seems so SQL data-like though to be converting this object (the board) into a string.
Wait. Why don't I just use the actual board? I mean, yes it's a like a one-hot,
...as mentioned before, but honestly, then I can just use the board of the game!
Totally makes sense.
No wait, but since it's a list, I can't use it as an index easily.
String is the best choice.
'''