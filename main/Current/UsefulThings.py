import sys
def assertPython3():   
    assert sys.version_info[0] >= 3, "Python version needs to be at least 3"

def printAndReturn(val):
    #print(val)
    return val

def askYesOrNo(question):
    assertPython3() #upgrade: the below attempt at compatibility failed, so I'm doing this
    '''
    #Python 2 compatibility
    try:
        input = raw_input
    except NameError:
        pass
    '''

    while True:
        ans = input(question+" (y/n) ").lower()
        if ans in ['y', 'yes', 'yeah', 'yep']:
            return True
        elif ans in ['n', 'no', 'nope', 'nah']:
            return False
        else:
            print("Answer was not 'y' or 'n'.")

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
        

class TimeoutExpired(RuntimeError):
    pass

def alarm_handler(signum, frame):
    raise TimeoutExpired

import signal
def timeoutInput(prompt, timeout):
    # set signal handler
    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(timeout) # produce SIGALRM in `timeout` seconds

    try:
        return input(prompt)
    finally:
        signal.alarm(0) # cancel alarm
    
if __name__ == "__main__":
    timeoutInput("Hello ", .5)
    