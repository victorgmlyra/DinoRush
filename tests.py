import numpy as np
import neuralNet

def funct(x):
    return x/(1 + abs(x))

# a = [1.78888221, 1.08454306]
# print([neuralNet.fast_sigmoid(i) for i in a])

b = np.matrix([1, 1, 1])
print(np.append(b, [[1]], axis=1))
