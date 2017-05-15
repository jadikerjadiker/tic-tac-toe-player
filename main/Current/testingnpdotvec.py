import numpy as np
import UsefulThings as useful


@useful.supressWarnings
@np.vectorize
def reciprocal(num):
    try:
        return 1/num
    except ZeroDivisionError:
        return 0
    
reciprocal(0)
    
    