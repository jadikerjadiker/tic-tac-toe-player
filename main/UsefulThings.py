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

#If you're running a for loop like
#'for i in range(maxVal)'
#Then in the loop you can run printPercent(i, maxVal)
#...to print the percentage that the loop is done
#This doens't work perfectly because of rounding error, but it's close enough.
#(Sometimes it will skip or double print a number)
def printPercent(indexNumber, outOf, incrementAmt = 1, roundAmt = 0):  
    printPc = 100.0*(indexNumber+1)/outOf
    if printPc%incrementAmt<(100.0/outOf):
        print("{}%...".format(round(printPc, roundAmt)))