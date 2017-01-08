import sys

def printAndReturn(val):
    #print(val)
    return val
    
def askYesOrNo(question):
    while True:
        try:
            ans = raw_input(question+" (y/n) ").lower()
            if ans in ['y', 'yes', 'yeah', 'yep']:
                return True
            elif ans in ['n', 'no', 'nope']:
                return False
            else:
                raise RuntimeError("Bad input")
        except:
            print("Answer was not 'y' or 'n'.")

def assertPython3():   
    assert sys.version_info[0] >= 3, "Python version needs to be at least 3"
  
def printPercent(indexNumber, outOf, logAmt = 1, incrementAmt = 1, roundAmt = 1):  
    printPc = 100.0*(indexNumber+1)/outOf
    if printPc%logAmt<incrementAmt:
        print("{}%...".format(round(printPc, roundAmt)))
