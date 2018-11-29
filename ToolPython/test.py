import numpy as np

x = [-2.5,2,-4.5,5,3,2,2,3]

def argmedian(x):
    x1 = [i for i in x if str(i) != 'nan']
    arg_median = np.argsort(x)[len(x1)//2]
    return(arg_median)

print(np.nanmedian(x))
print(argmedian(x))
