import random
import numpy as np


# Activation functions
def relu(x):
    return x if x > 0 else 0

def fast_sigmoid(x):
    return x/(1 + abs(x))

class neuralNet:
    
    # Create a random neural network fully connected with num inputs and num outputs
    # hidden_layers is a list which every element is teh number of neurons of a hidden layer
    def __init__(self, num_inputs, num_outputs, hidden_layers = []):
        self.network = []
        for i, neurons in enumerate(hidden_layers):
            if i == 0:
                self.network.append(np.random.randn(num_inputs + 1, neurons)) # Matrix containing wheights and biases
            else:
                self.network.append(np.random.randn(hidden_layers[i-1] + 1, neurons))

        if len(hidden_layers) > 0:
            self.network.append(np.random.randn(hidden_layers[-1] + 1, num_outputs))
        else:
            self.network.append(np.random.randn(num_inputs + 1, num_outputs))

    # Run Neural Network with given input
    def run(self, inputs):
        out = np.matrix(inputs)
        for layer in self.network:
            out = np.append(out, [[1]], axis=1)
            out = out * np.matrix(layer)
            out = fast_sigmoid(out)
        return out
        

rede = neuralNet(2, 2)
print(rede.run([1, 1]))
print()
print(rede.network)
