import numpy as np
import math #for e^x (math.exp())

#This thing causes some errors to pop up on the side of cloud9, you can just ignore them.  (This works, although I don't understand how or why at this point...)
@np.vectorize #turns it into a function that can be applied element-wise on a column vector
def sigmoid(num):
    return 1/(1+math.exp(-num))

def resizeToVector(thing):
    return np.resize(thing, (thing.size, 1))

def makeVector(thing):
    return resizeToVector(np.array(thing))
    
def insertColVecOnLeft(matrix, colVec):
    return np.insert(matrix, [0], colVec, axis=1)

'''
All a neural net is is a bunch of weights, going from one layer to the next
'''
class NeuralNet:
    def __init__(self, architecture):
        self.architecture = architecture
        #create matricies with random values with the correct dimensions (n(l) x n(l-1)+1)
        self.net = [np.random.randn(self.architecture[layerIndex], self.architecture[layerIndex-1]+1) for layerIndex in range(1, len(self.architecture))]
    
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
            
        assert len(inpt)==self.architecture[0], "Input must have the correct number of values. (In this case, {} values.)".format(self.architecture[0])
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
    
    def getErrorOfLastLayer(self, inpt, solution):
        return self.run(inpt)-makeVector(solution)
    
    #back propagation
    #batch is a list of tuples [(vector-like input, vector-like solution), (vector-like input, vector-like solution), ...]
    def backProp(self, batch, normalization = 1, runTime = 1):
        delta = [np.zeros((self.architecture[layerIndex], self.architecture[layerIndex-1]+1)) for layerIndex in range(1, len(self.architecture))]
        for iteration in range(runTime):
            for trainingExample in batch:
                errors = []
                #a is a list of activation vectors, the first vector is the one from the second layer.
                #print("trainingExample:\n{}".format(trainingExample))
                activations = self.getActivations(trainingExample[0])
                #print("architecture:\n{}".format(self.architecture))
                #print("Getting activations finished.")
                #print("Net:\n{}".format(self))
                y = makeVector(trainingExample[1])
                #calculate the error in the last layer
                lastLayerError = activations[-1]-y
                error = np.array(lastLayerError)
                errors.append(error)
                #go backwards through each layer of the net and calculate the error for those
                #i = (number of layer we're computing the error for) - 1
                #i is basically just converting from computer to human numbers
                #starts at the second to last layer and goes all the way to the input layer
                #(even though it doesn't need to calculate the error of the input layer)
                #remember, here, we ignore the bias values in the weight matrix
                for i in range(len(self.architecture)-2, -1, -1):
                    #print(i)
                    #print("activations:\n{}".format(activations))
                    #get the activation value of the layer I'm computing the error for
                    activation = activations[i]
                    #we have the activation value of our layer
                    #and the error of the layer in front of us
                    #so we can compute the derivative and add it to delta
                    #print("error:\n{}".format(error))
                    #print("activation:\n{}".format(activation))
                    deltaChangeWithoutBias = np.matmul(error, np.transpose(activation))
                    #print("deltaChangeWithoutBias:\n{}".format(deltaChangeWithoutBias))
                    deltaChange = np.insert(deltaChangeWithoutBias, 0, error.flatten(), axis = 1)
                    #print("deltaChange:\n{}".format(deltaChange))
                    delta[i] = np.add(delta[i], deltaChange)
                    #print("weightMatrix:\n{}".format(self.net[i]))
                    #take out the bias from the weight matrix going from this layer to the next layer
                    noBiasWeightMatrix = np.delete(self.net[i], 0, 1)
                    #print("activation:\n{}".format(activation))
                    #print("noBiasWeightMatrix:\n{}".format(noBiasWeightMatrix))
                    #print("error:\n{}".format(error))
                    #step1 = np.matmul(np.transpose(noBiasWeightMatrix), error) #should give n(l) x 1
                    #print("activationDerivative:\n{}".format(activationDerivative))
                    #print("activation:\n{}".format(activation))
                    #step2 = np.multiply(activationDerivative, activation)
                    #follow the formula to compute the error of the layer
                    error = np.multiply(np.multiply(np.matmul(np.transpose(noBiasWeightMatrix), error), activation), np.subtract(np.ones(activation.shape), activation))
                    #print("Error:\n{}".format(error))
                    errors.insert(0, error)
                    #weightTranspose = np.transpose()
                
                #update the weights
                for matrixIndex in range(len(self.net)):
                    self.net[matrixIndex] = np.subtract(self.net[matrixIndex], delta[matrixIndex])
                print("Iteration {}".format(iteration+1))
                print("All errors:\n{}".format(errors))
                print("Final gradient amount:\n{}".format(delta))
    
    def __str__(self):
        ans = "Weights:\n"
        for i, val in enumerate(self.net):
            ans+=str(val)+"\n"
        return ans

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

    training = ([1, 2, 3], [1, 0])
    n = NeuralNet([3, 4, 3, 2])
    w = n.net[0]
    import copy
    oldMatrix = copy.deepcopy(n.net)
    beforeResponse = n.run(training[0])
    beforeError = n.getErrorOfLastLayer(*training)
    n.backProp([training], runTime = 400)
    print("beforeResponse:\n{}\nnewResponse:\n{}\nbeforeError:\n{}\nnewError:\n{}".format(beforeResponse, n.run(training[0]), beforeError, n.getErrorOfLastLayer(*training)))
    #print(oldMatrix)
    #print(n.net)
