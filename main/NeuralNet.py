import numpy as np
import math #for e^x (math.exp())

#This thing causes some errors to pop up on the side of cloud9, you can just ignore them.  (This works, although I don't understand how or why at this point...)
@np.vectorize #turns it into a function that can be applied element-wise on a column vector
def sigmoid(num):
    try:
        return 1/(1+math.exp(-num))
    except OverflowError:
        if num<100:
            return 0
        elif num>100:
            return 1
        else:
            print("Here's the number that caused the error:{}".format(num))
            raise

def resizeToVector(thing):
    return np.resize(thing, (thing.size, 1))

def makeVector(thing):
    return resizeToVector(np.array(thing))

'''
All a neural net is is a bunch of weights, going from one layer to the next
'''
class NeuralNet:
    def __init__(self, architecture):
        self.architecture = architecture
        #create matricies with random values with the correct dimensions (n(l) x n(l-1)+1)
        self.net = [np.random.randn(self.architecture[layerIndex], self.architecture[layerIndex-1]+1) for layerIndex in range(1, len(self.architecture))]
    
    def __str__(self):
        ans = "Weights:\n"
        for i, val in enumerate(self.net):
            ans+=str(val)+"\n"
        return ans
    
    #returns the output of the neural net as a vector
    def run(self, inpt):
        return self.getActivations(inpt)[-1]
    
    #forward propagation
    #takes a vector-like object as input
    #returns a list with elements equal to the number of layers in the net...
    #[activationVector of input layer, activationVector of first hidden layer, etc.]
    def getActivations(self, inpt):
        #insert the bias of 1 at position 0 in the array and turn it into a vector
        def insertBias(inpt):
            return np.insert(inpt, [0], [[1]], axis = 0)
            
        assert len(inpt)==self.architecture[0], "Input\n{}\nmust have the correct number of values. (In this case, {} values.)".format(inpt, self.architecture[0])
        inpt = makeVector(inpt)
        activations = [inpt]
        for weightMatrix in self.net:
            #print("inpt: {}".format(inpt))
            #print("matrix: {}".format(weightMatrix))
            #First, insert the bias into the input vector
            #Then, multiply the vector by the weightMatrix
            #Then, apply the sigmoid function
            #Then, add the resultant activation vector to the activations list
            inpt = sigmoid(np.matmul(weightMatrix, insertBias(inpt))) 
            activations.append(inpt)
        
        return activations
    
    #return the error of the final layer (a vector) given the input and the wanted result
    def getFinalError(self, inpt, solution):
        return self.run(inpt)-makeVector(solution)
    
    #back propagation
    #a batch is a list of tuples [(vector-like input, vector-like solution), (vector-like input, vector-like solution), ...]
    #batches is a list of batches [batch1, batch2, etc.]
    #mode is a tuple (modeType, modeValue)
    #Here are the different modes in order of how much error they allow. Less error is at the top:
    #modeType: what modeValue does (this is an example)
    #"iter": value specifies the amount of times the training is done
    #"avg": value specifies the maximum average error allowed over the each example
    #"avgAvg": value specifies the maximum allowed sum of the averages of the error in each example of the batch
    #"specific": value specifies the maximum average error allowed for each output neuron on each example
    #The net will continue to train on the entire batch until the error is low enough or it has trained enough times (depending on the mode)
    #TODO use normal expressions like '-' and '+' when possible
    def train(self, batches, learningRate = 1, mode = ("iter", 1), trainAway = False):
        def trainBatch(batch, learningRate, mode, trainAway):
            #returns an ordered list of vectors where each vector is the output error for the example in the batch
            def getOutputErrors(batch):
                ans = []
                for trainingExample in batch:
                    ans.append(self.getFinalError(*trainingExample))
                return ans
             
            #returns True if every value in item (or item itself if item is just a number) is lower or equal to value.
            #returns False otherwise
            def checkLessOrEqualTo(item, value):
                if hasattr(item, '__iter__'): #item is a list
                    for val in item:
                        if val>value:
                            return False
                else: #item is a number
                    if item>value:
                        return False
                return True
                
            #returns a new list that just averages each output error vector from outputErrors
            #assumes that each error vector has the same shape
            def avgExampleErrors(outputErrors):
                outputNeuronAmt = outputErrors[0].shape[0]
                return [np.sum(val)*1.0/outputNeuronAmt for val in outputErrors]
                
            def avgBatchError(outputErrors):
                return sum(avgExampleErrors(outputErrors))*1.0/len(outputErrors)
                
            while True: #continue training on the batch until its mode tells it to return
                modeType, modeValue = mode #separate the mode out into the type and value
                outputErrors = getOutputErrors(batch) #returns an ordered list of vectors where each vector is the output error for an example in the batch
                positiveOutputErrors = [np.absolute(outputError) for outputError in outputErrors]
                if modeType=="iter": #modeValue is the counter as to how many times the training should run
                    if modeValue<=0:
                        return
                    else:
                        modeValue-=1
                elif modeType=="avg":
                    if checkLessOrEqualTo(avgExampleErrors(positiveOutputErrors), modeValue):
                       return
                elif modeType=="avgAvg":
                    if checkLessOrEqualTo(avgBatchError(positiveOutputErrors), modeValue):
                        return
                elif modeType=="specific":
                    #go through each outputError
                    for outputError in positiveOutputErrors:
                        #make sure that outputError has no values greater than the modeValue
                        if checkLessOrEqualTo(np.nditer(outputError), modeValue):
                            return
                else:
                    raise RuntimeError("Unrecognized mode type '{}'".format(modeType))
                        
                #The list containing the matricies of derivatives. At the end we subtract these matricies from the weight matricies
                #So you can also think of this as the list of matricies of how much the weights need to change
                #delta[l-1] is the delta matrix that matches with the weight matrix that goes from layer l to layer l+1
                delta = [np.zeros((self.architecture[layerIndex], self.architecture[layerIndex-1]+1)) for layerIndex in range(1, len(self.architecture))]
                for exampleNum, trainingExample in enumerate(batch):
                    error = outputErrors[exampleNum]
                    #list of errors in each layer. errors[l-1] is the error of layer l
                    errors = [error]
                    #activations is the list of activation vectors, the first vector is the one from the input layer (which can be negative and greater than 1).
                    activations = self.getActivations(trainingExample[0])
                    
                    #go backwards through each layer of the net and calculate the error for those
                    #i = (number of layer we're computing the error for) - 1
                    #i is basically just converting from computer to human numbers
                    #starts at the second to last layer and goes all the way to the input layer
                    #(even though it doesn't really need to calculate the error of the input layer)
                    #remember, here, we ignore the bias values in the weight matrix
                    for i in range(len(self.architecture)-2, -1, -1):
                        #get the activation values of the layer whose error is being computed
                        activation = activations[i]
                        
                        #we have the activation value of our layer
                        #and the error of the layer in front of us
                        #so now we can compute the derivative
                        #and add it to delta
                        
                        #Compute the delta, following the formula
                        deltaChangeWithoutBias = np.matmul(error, np.transpose(activation))
                        #insert in the delta values for the bias (which is just the error of the layer) as the first column in the matrix
                        deltaChange = np.insert(deltaChangeWithoutBias, 0, error.flatten(), axis = 1)
                        #add this deltaChange to the total delta (this is what makes it batch training; the mini deltas are added up)
                        delta[i] = np.add(delta[i], deltaChange)
                        
                        
                        #take out the bias from the weight matrix going from this layer to the next layer so we can compute the error
                        noBiasWeightMatrix = np.delete(self.net[i], 0, 1)
                        #follow the formula to compute the error of the next layer back
                        error = np.multiply(np.multiply(np.matmul(np.transpose(noBiasWeightMatrix), error), activation), np.subtract(np.ones(activation.shape), activation))
                        
                        #add this error to the start of errors
                        errors.insert(0, error)
    
                    #update the weights
                    for matrixIndex in range(len(self.net)):
                        if trainAway:
                            funcToUse = np.add #want to train it away from the example, so we add the error
                        else:
                            funcToUse = np.subtract #want to train it towards the example, so we subtract the error
                        self.net[matrixIndex] = funcToUse(self.net[matrixIndex], np.multiply(learningRate, delta[matrixIndex]))
        
        #This is the main part of the function that actually runs
        for batch in batches:
            trainBatch(batch, learningRate, mode, trainAway)
            
    
    

if __name__ == "__main__":
    '''
    a = [1, 2, 3]
    a = makeVector(a)
    print(a)
    print(np.insert(a, [0], [[1]], axis = 0))
    '''
    '''
    a = np.array([])
    b = [[1, 2, 3], [3, 2, 1], [1, 1, 1]]
    
    a = np.insert(a, [0], [[1],[2],[3]], axis=1)
    print(a)
    '''
    '''
    for i in range(len([4, 6, 7, 8])-1, 0, -1):
        print(i)
    '''    
    '''
    a = np.array(a)
    b = np.array(b)
    print(a)
    print(b)
    a = resizeToVector(a)
    b = resizeToVector(b)
    print(a)
    print(b)
    a = makeVector(a)
    b = makeVector(b)
    print(a)
    print(b)
    print(a-b)
    '''
    '''
    n = NeuralNet([9, 3, 3, 2])
    print(n)
    a = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    print("Activations:\n{}".format(n.getActivations(a)))
    print("Run:\n{}".format(n.run(a)))
    n.backProp([([1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 1])])
    '''


    training = ([1, 1, 0, -1, -1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0])
    n = NeuralNet([9, 9, 9, 9])
    w = n.net[0]
    import copy
    oldMatrix = copy.deepcopy(n.net)
    beforeResponse = n.run(training[0])
    beforeError = n.getFinalError(*training)
    n.train([[training]], learningRate = 1, mode = ('avg', .001))
    print("beforeResponse:\n{}\nnewResponse:\n{}\nbeforeError:\n{}\nnewError:\n{}".format(beforeResponse, n.run(training[0]), beforeError, n.getFinalError(*training)))
    #print(oldMatrix)
    #print(n.net)
