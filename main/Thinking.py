#This was originally created in the 'firstworkspace' workspace.
#It was transfered to a new workspace on 12/7/2016

'''
12/4/16

I want to create a computer that will learn strategies for games and play them well.
I figured a good place to start would be with tic-tac-toe.

How do humans do it?

Well, first you have to know how the game is played and how to win the game.
Then, you watch people play, or you play yourself, and you judge usually based on some heuristic, how likely someone is to win the game.

For example, if someone has a fork in tic-tac-toe, they're probably likely to win the game.
Same if someone has two in a row.

In crazy eights, it would be having less cards in your hand.

Usually, it's whatever gets you closer to winning that you watch.

So how would a computer figure out what makes you closer to winning just by knowing the objective?

Well, humans usually run through the games backwards in their mind.
In tic-tac-toe, you know that 3 in a row is one step away from 2 in a row.

So a computer would simulate a game position with one player winning,...
and then try to emulate that player and progress backwards through a game.
More likely, a computer would play through a game randomly, look at who won at the end, and then try to be more like that random player.

So what if you gave it a neural net.
It plays through a game, and then updates itself to play as the winner, based on the board.

For tic-tac-toe, this is easy. Only 9 inputs, trains itself on each step of the game to play as the winner did.
In case of a tie, don't train at all.

Then, generate a new game, and train yourself until you play that one to win as well.
Then, go back and train on the old ones and make sure you still win those.
If not, train on those, then come back and train on the new one, then train on those, etc. until they both work.
If you go through that iteration a certain amount of times, stop. (In later versions, this may cause it to create a new layer)

Then, repeat this cycle for a certain amount of times, and then play against the human to see how well you do.

In a later version, after generating enough random games, it will play itself against a random game in a set.
If it wins much more than it loses, then it starts to play itself, adding in a random game, and a random shift on a game,
every once in a while.


What I need:
A representation of the game, and a representation of a played game.
A neural net and a method to be given a game and train itself to be the winner.
An overall method running this plan.
'''

'''
I think the next net should either train on ties as well
or play against a random computer.

I think playing against a random player will be more interesting result-wise, so I'll do that next.

I'm also judging how good these nets are based on one situation.
I have also yet to implement bigger batches than one game.

I'm also just making sure the average error over each batch is below a certain level.
What if the error of each had to be below a certain level?
'''