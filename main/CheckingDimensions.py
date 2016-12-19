'''
I have now figured out how this works, so I will outline it here.

First, the definitions.

There are L layers in the network, where layer 1 is the input layer. l usually stands in for a layer in general.
n(l) will be used as shorthand to represent the neurons in the lth layer (not including bias).

'activations' (a) is a list so that activations[l-2] is the activation vector of the l'th layer (with no bias)
The dimension of activations[l-2] is n(l) x 1
activations[0] is the vector of activations for the first non-input layer (the second layer).

'errors' (the curvy d-looking, or lowercase delta) is a list so that errors[l-2] is the vector of error for the l'th layer.
The dimension of errors[l-2] is n(l) x 1 (the bias is not included in the error)
errors[0] gives the error of the first non-input layer.

'weights' (theta) is a list of matricies such that the weights[l-1] is the matrix to convert the activations and bias from layer l into the input to the (l+1)th layer
The dimension of weights[l-1] is n(l+1) x n(l)+1
weights[0] is the matrix of weights going from the input layer to the the first hidden layer (without the bias).

'delta' (the triangle or capital delta) is a list of matricies such that delta[l-1] is the matrix of derivatives from layer l (with bias) to the (l+1)th layer
It's what you should subtract from the weights when you update.
The dimension of delta[l-1] is n(l+1) x n(l)+1

When writing equations or using symbols,
(wb) means "with bias"
(wob) means "without bias"
d is the partial derivative symbol
e is the error or 'errors'
C is the cost
s is the sigmoid function
z is activations before sigmoid
w is the weights or 'weights'
dlt is 'delta'
a=s(z) is the activations after sigmoid (wob), or 'activations'

The definition of e:
e = dC/dz


The first formula is confusing because we're immediatlely ignoring the definition of e.
Really, we should be doing something a bit more complicated here, but this is simpler so we're just doing this.
Overall, I think the algorithm still works (and maybe given our cost function, this is what it simplifies to).
The error of the Lth layer turns out to seem like it's just common sense.
You take the activations of the last layer (and don't count the bias in the activations) and subtract the vector of the answer you should have gotten.
The formula is e[L-2] = a[L-2]-answerVector with dimension n(L) x 1
Boom. Done.

[
These brackets contain the complicated stuff we shoulda done.
Error can also be written as
e = dC/da * s'(z) (explained below)

So,
e[L-2] = dC/d(a[L-2]) * s'(z) (we don't even keep track of z!)
is what we should be calculating.
It just may so happen that that expression simplifies to a[L-2] - answerVector
But I think it's probably likely that a[L-2] is just a good enough estimate that it works.
]

The next formula is how to compute the error of previous layers.
Note that the definition of error is the derivative of the cost with respect to the activations before the sigmoid function has been applied.
Therefore, by the chain rule, the error is equal to the derivative of the cost, with respect to the activations with the sigmoid function applied times...
the derivative of the activations with the sigmoid function applied with respect to the activations without the sigmoid function applied.
The above line simplifies to 'the derivative of the sigmoid function'.

Here's it in equations:
Let e be the error, C be the cost, s be the sigmoid function, z be activations before sigmoid, and a=s(z) be the activations after sigmoid.
e = dC/dz (by definition of e) = dC/da * da/dz (by chain rule) = dC/da * d[s(z)]/dz (by definition of a) = dC/da * s'(z) (be definition of derivative)


'''
'''
Okay, so looking at more stuff, it seems like we are totally ignoring the bias when using backprop. So what would the dimensions look like if I did that?

There are L layers in the network, where layer 1 is the input layer. l usually stands in for a layer in general.
n(l) will be used as shorthand to represent the neurons in the lth layer (not including bias).

'activations' (a) is a list so that activations[l-2] is the activation vector of the l'th layer without the bias
The dimension of activations[l-2] is n(l) x 1
activations[0] is the vector of activations for the first non-input layer (the second layer).

'errors' (the curvy d-looking, or lowercase delta) is a list so that errors[l-2] is the vector of error for the l'th layer.
The dimension of errors[l-2] is n(l) x 1
errors[0] gives the error of the first non-input layer.

'weights' (theta) is a list of matricies such that the weights[l-1] is the matrix to convert the activations but NOT bias from layer l into the input to the (l+1)th layer
The dimension of weights[l-1] is n(l+1) x n(l)
weights[0] is the matrix of weights going from the input layer to the the first hidden layer (without the bias).

'delta' (the triangle or capital delta) is a list of matricies, so that delta[l-2]

So we initialize the error of the last layer. Each error we create we insert into errors at 0.
This error will be a vector with dimension equal to the amount of output neurons (neurons in the Lth layer).

The next formula we have is (error of lth layer) = 
(transpose((lth layer's weights))(error of (l+1)th layer)) element multiplied by l'th layer's activations element multiplied by (1-(l'th layer's activations))

So with the indexes I have, errors[l-2] = (np.transpose(weights[l-1])(errors[l-1])).*activations[l-2].*(1-activations[l-2])

Which will have dimension n(l) x 1 = transpose(n(l+1) x n(l))(n(l+1) x 1).*(n(l) x 1).*(n(l) x 1)

which is odd, but works.

Okay, so I found these resources:
https://mattmazur.com/2015/03/17/a-step-by-step-backpropagation-example/
http://stackoverflow.com/questions/3775032/how-to-update-the-bias-in-neural-network-backpropagation
ftp://ftp.sas.com/pub/neural/FAQ2.html#A_bias
http://stats.stackexchange.com/questions/130158/backpropagation-bias-nodes-and-error

I still don't understand what I'm updating them with, but at least I know now that dim(errors[l-2]) = n(l) x 1

Let's figure out the next part.

They give me (layer l of delta) = layer l of delta + (error of layer l+1)transpose(activations of layer l)

which works out because that multiplication on the end becomes (n(l+1) x 1) (1 x n(l))
so layer l of delta is just a n(l+1) by n(l) matrix: same dimension as the weights.

So uppercase delta is how much the weights should change by. You multiply the activation by the error to get the derivative/how much it should change.
'''

'''
I was going to do this on paper, but I know that paper gets lost very easily and I won't always have it when working on the project then.

So the goal here is to understand the dimensions of all of these vectors and things to make sure I get this working right.

There are L layers in the network, where layer 1 is the input layer. l usually stands in for a layer in general.
n(l) will be used as shorthand to represent the neurons in the lth layer.

'delta' (the triangle delta) is a list of delta_i,j so that delta[0] = (delta^1)_i,j #TODO not sure about this yet

'activations' (a) is a list so that activations[l-2] is the activation vector of the l'th layer with the bias inserted
The dimension of activations[l-2] is n(l)+1 x 1
activations[0] is the vector of activations for the first non-input layer (the second layer).


'errors' (the curvy d-looking delta) is a list so that errors[l-2] is the vector of error for the l'th layer.
The dimension of errors[l-2] is n(l) x 1
errors[0] gives the error of the first non-input layer.


'weights' (theta) is a list of matricies such that the weights[l-1] is the matrix to convert the activations and bias from layer l into the input to the (l+1)th layer
The dimension of weights[l-1] is n(l+1) x n(l)+1
weights[0] is the matrix of weights going from the input layer to the the first hidden layer.

So we initialize the error of the last layer. Each error we create we insert into errors at 0. This error will be a vector with dimension equal to the amount of output neurons (neurons in the Lth layer).

The next formula we have is (error of lth layer) = (transpose((lth layer's weights))(error of (l+1)th layer)) element multiplied by l'th layer's activations element multiplied by (1-(l'th layer's activations))

So with the indexes I have, errors[l-2] = (np.transpose(weights[l-1])(errors[l-1])).*activations[l-2].*(1-activations[l-2])

This will be n(l) x 1 = transpose(n(l+1) x n(l)+1)(n(l+1) x 1).*(n(l)+1 x 1).*(n(l)+1 x 1)

which becomes (n(l)+1 x n(l+1))(n(l+1) x 1).*(n(l)+1 x 1) x (n(l)+1 x 1) which gives a final result of (n(l)+1 x 1)

So does the error vector give an error for the bias that we basically just ignore? How does this work?
'''