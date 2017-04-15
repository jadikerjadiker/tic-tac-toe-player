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

'''
So here are the things I've come up with that are parameters for the neural networks

Architecture
Type of training
    'iter' only train on each batch a certain amount of times
    'batchError' train until the average error on the batch is less than a certain amount
    'totalBatchError' train until the total error on the batch is less than a certain amount
    'exactError' train until error on each output neuron for each example is less than a certain amount
    'exampleError' train until the average error on each example in the batch is less than a certain amount
    'totalExampleError' train until the total error on each example in the batch is less than a certain amount
Amount of error/times to train on batch
Learning rate
Examples per batch
Which games are trained on (winner, ties, loser?)
Number of games trained on
How the games the net learns from are created
    Any combination (2 of the following 5) of
        Human
        Random
        Random net
        Non-random net (so many different options)
        self
    which gives 10 possible ways to train it. I can also train on any combination of these 10.
    
So I have 11 different things I can change, most with an infinite amount of options associated with them.
'''

'''
For the batch error, is it the sum of the averages, the averages of the sum, the sum of the sums, or the averages of the averages?
Are they all different things? Or are some of them equivalent?

Lets call the vectors of error e1, e2, etc. 
And the list of errors E = [e1, e2, etc]
a(e1) is the average of e1 and s(e1) is the sum of e1

Note that a(e1) = s(e1)/len(e) = s(e1)/9 (for output dimension of 9)

sum of averages:
s([a(e1), a(e2), etc]) = s([s(e1)/len(e), s(e2)/len(e), etc]) = s([s(e1), s(e2), etc])/len(e)

average of sums:
a([s(e1), s(e2), etc]) = s([s(e1), s(e2), etc])/len(E)

average of averages:
a([a(e1), a(e2), etc]) = a([s(e1)/len(e), s(e2)/len(e), etc]) = s([s(e1)/len(e), s(e2)/len(e), etc])/len(E) = s([s(e1), s(e2), etc])/(len(e)len(E))

sum of sums:
s([s(e1), s(e2), etc])

So it looks like it really just depends on how accurate you want it to be.
sum of sums is the most accurate
sum of averages will be more accurate (than average of sums) if you have a batch bigger than len(e) (which is often the case)
average of sums will be less accurate (than sum of averages) if you have a batch bigger than len(e) (which is often the case)
average of averages is the least accurate

The average of sums means you have to train really well on some examples in order to have examples that aren't trained so well.
The sum of averages means you have to be more accurate on each individual example.

But yes, they are all different.

Oh wow. I also have "specific error" which means that none of the error can be less than a certain amount. You don't get a value for the entire batch.
In other words, it forces the entire batch to be trained to a specific level.
'''

'''
Here's the question I asked on cross-validated (http://stats.stackexchange.com/questions/253050/most-common-method-for-deciding-when-to-stop-training-a-neural-net-on-a-batch)

I have created my own neural net which is using stochastic gradient descent. In other words, it trains on batches of examples all at once.

My issue is trying to figure out when to stop the training of the batch. I'll try to make things as understandable as possible since there are so many options, but please comment if you need clarification.

Each batch allows me to compute a list of output errors that correspond to the error the computer has on each example. Each error is a vector with elements equal to the number of output neurons.

Let each error vector be notated by e1, e2, e3, ... so the list of output errors is [e1, e2, ...]. Let an error vector in general be notated by e.

Also, let us define len() to be a function which returns the amount of elements in a vector or list. For example, len(e) is the amount of output neurons in the neural network.

Now there are 3 things we can do to a vector or a list:

Sum: add up all of the elements in the vector or list. This will be notated by the function s(). For example, s(e) would be totaling the error found in error vector e.
Average: average all of the elements in a vector of list. This will be notated by the function a(). For example, a(e) = s(e)/len(e)
Check: make sure that each element in the vector or list is below a certain value. If any of the elements are too high, we continue to train on the entire batch. (This function can also be applied to a single value.) This will be notated by the function c(). For example, if we wanted to make sure the total error in e was low enough, we would do c(s(e))

Here are the methods I have determined for deciding when to stop gradient descent:

Iterative: just run the training a certain number of times
Sum of sums: Total up all the error in the entire batch and then make sure it's low enough. This is given by the formula c(s([s(e1), s(e2), ...])
Sum of averages: Find the average error of each example, then add up all those and make sure it's below a certain amount. This is given by the formula c(s([a(e1), a(e2), ...]))
Average of averages: Find the average error of each example, then find the average of those and make sure it's below a certain amount. This is given by the formula c(a([a(e1), a(e2), ...]))
Average of sums: Compute the average total error in each example, and then make sure it's below a certain amount. This is given by the formula c(a([s(e1), s(e2), ...]))
Specific error: Check to make sure the error in each output neuron is below a certain amount. This is given by the formula c(e1), c(e2), ...
Specific sums: Check to make sure the total of the error in each example is below a certain amount. This is given by the formula c([s(e1), s(e2), ...])
Specific averages: Check to make sure the average error in each example is below a certain amount. This is given by the formula c([a(e1), a(e2), ...])
So my question is this:

Which one of these options is most commonly used when training neural nets? Why? (Is there another option that I've missed?)
'''

'''
Okay, I think I can implement all of these versions relatively easily actually.
The question is coming up with names for them.

sumSum
sumAvg
avgSum
avgAvg
sum
avg
specific
iter

There, that works.
'''

'''
Summing makes no sense because if you're going to have different batch sizes, the sum will be very different for those sizes.
And if you're not going to have different batch sizes, you can just use the average.
So, I'm getting rid of 'sumAvg', 'avgSum', 'sumSum', and 'sum'
'''

'''
An idea that I had before that I think would work well but hadn't written down is that...
there should be multiple nets, each one training on a certain number move.
So the first net trains on the first move, second net trains on the second move, etc.

I think we'll get better results that way, much like the 2-lane road needed a different net...
to drive than the 1-lane road in the Coursera video example
'''

'''
The way I've been doing this so far has been really not that smart.

I've been expecting the computer to learn from random games, and training to play as the winner
But honestly, at the start of the game, the random players make really stupid moves.
So training them to play at the start like the random players do is just really bad.

Right now, the best thing I can think of is to allow a high amount of error...
so that it can unlearn bad moves at the start.
But I'm pretty sure that won't work either. Idk how I'm going to do this.
It's an interesting problem.
'''

'''
Similar to that last block of thinking, after more experimentation I've found my implementation probably isn't wrong.

Even though it's training towards the data it still sometimes performs worse (on its own training set).

So while that is odd, I think it's mainly because the data makes no sense.

I'm having it play random games. These random games make no sense as to why one would allow you to win,...
as opposed to another.
A human learning to play from these games would be comfused as well...
since they probably contain at least two completely contradictory examples where one says one way is correct and the other says the other way is correct.

In short, the computer is learning from terrible players who don't know what they're doing.

So how do I get some good data for the computer to learn from?

One way is to have it play against a human, or create my own set of data and see how it does.

But the thing that's interesting to me is not to see if it can learn from the best and be the best,...
but if it can learn from the worst and be the best.

So how do I get it to learn better?

I want it to only know what a win is and what a loss is and go from there.
'''

'''
So I've looked up how Alpha Go works, and some machine learning techniques, especially reinforcement learning.

It seems like the way to go is to use a neural net to train on a policy set using Sutton and Barto's work.

Then, if I want to go super far, be like Google and train two neural policy networks and have them play against each other mostly greedily.

Use those values to update as well.

Then, find some combo of the two that seems to work.

Maybe one of the nets is really big and the other is really small, so one goes fast and the other is a tiny bit slower, kinda like Google's?

Idk yet.
'''

'''
As difficult as I think it will be, I think I should switch everything to be player 0 and player 1, not 1 and -1.
I don't know why I made such a bad decision in the first place.
At the same time though, I think it will be faster for me to just keep it than it will for me to go back and fix it.

So, the goal right now is to set it on solving Chopsticks, and then switch the player numbers to 0 and 1
'''

'''
April 11 2017

I think I'm going to change what I'm doing for a little bit.

Originally, I thought I would teach it another game or have it learn from past learning, which I have done.
(You can now save and load policy players and have them continue their learning)
(I also taught it chopsticks, which it learns fairly quickly.)

So now, I want to use both the neural network and policy player together, much like Google did with Alpha Go
The neural net will train on the policy player and try to emulate it, and then play based off of those guessed policies.

I wonder if there's some way to measure confidence, that way if the net is unconfident, I can use the policy player more on that instance.
Just looked it up, and it doesn't seem like there's an easy way:
http://stats.stackexchange.com/questions/247551/how-to-determine-the-confidence-of-a-neural-network-prediction?noredirect=1&lq=1

Okay, so we just go with what we've got.
'''