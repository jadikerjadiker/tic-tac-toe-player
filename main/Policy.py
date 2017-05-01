import random

class UncreatablePolicy(RuntimeError):
    def __init__(self):
        RuntimeError.__init__("Was not given a board with which to create a new policy.")
        
class NonExistantPolicy(RuntimeError):
    pass

#basically just a fancy dict that stores the value of choosing each action at a particular state
#a single policy only keeps track of possible actions in a single state
#It can suggest values to choose and be greedy (choose its 'best' option) or
#...have a probability of exploring (choosing a 'non-best' option)
class Policy:
    #possActions is a list of actions that are actually choosable when suggesting
    #defaultValue is the default value for choosing each action
    def __init__(self, possActions, defaultValue = 0):
        self.values = {} #the dict to store the value of choosing each action
        self.possActions = possActions #a list of all the moves this policy has to keep track of
        self.defaultValue = defaultValue
        for action in possActions:
            self.values[action] = self.defaultValue
       #print("final values ended up being {}".format(self.values))
    
    def __str__(self):
        return str(self.values)
    
    #If explore is false, return the greedy (highest) value in this policy
    #If explore is true, choose a random value that's not the greedy one
    def suggest(self, explore = False):
        #get the highest value in the policy
        greedy = self.values[max(self.values, key=self.values.get)]
        #create a list of the actions that have this highest value
        #these actions are called "greedy actions"
        greedyActions = [action for action in self.values if self.values[action]==greedy]
        #If it should explore and not be greedy
        if explore:
            try:
                #pick a random action that is not a greedy action
                return random.choice([action for action in self.values if not (action in greedyActions)])
            except IndexError: #If all the values are greedy
                #just move on and choose a random (greedy) action
                pass
        #choose a random action
        return random.choice(greedyActions)
        
    
    #the formula used is
    #old = old+learningRate*(target-old)
    #This moves old a fraction (learningRate) closer to the target.
    #If learningRate is 1, it moves it to the target.
    #If learningRate is 0, it does nothing.
    def update(self, value, target, learningRate):
        self.values[value]+=learningRate*(target-self.values[value])

