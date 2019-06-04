import random
import numpy as np 
import neuralNet as nn

# Recieves a list of tuples, which containing a NeuralNet and it's perspective fitness score
# Outputs a list of around 100 elements with the NeuralNets repeating by their probablity based on each fitness score
def create_probablity_list(placements):
    out = []
    total_fit = sum([k[1] for k in placements])
    for (net, fit) in placements:
        out.extend([net] * int(fit * 100 / total_fit))
    return out

# Recieves the probability list and returns 2 parents
def choose_parents(prob_list):
    return (random.choice(prob_list), random.choice(prob_list))

# Make a child network from 2 parents
# Output a neuralNet object with the new network
def crossover(parents):
    parent1 , parent2 = parents
    child_network = []
    for i in range(len(parent1.network)):
        temp_layer = parent1.network[i].copy()
        for j in range(temp_layer.shape[0]):
            temp_layer[j, :] = random.choice([parent1.network[i][j, :], parent2.network[i][j, :]])
        child_network.append(temp_layer)
    child = nn.neuralNet(0, 0)
    child.network = child_network
    return child

# Randomize a child gene with a certain probability
def mutate(child, prob_mutate):
    m = lambda x, prop_m : random.random()*2 - 1 if random.random() <= prop_m else x
    func = np.vectorize(m)
    for i in range(len(child.network)):
        child.network[i] = func(child.network[i], prob_mutate)

# Utilizes all functions above to create a new population
def create_new_population(placements, prob_mutate = 0.1):
    best_player = max(placements, key=lambda x: x[1])[0]
    prob_list = create_probablity_list(placements)
    new_pop = [best_player]
    for _ in range(len(placements) - 1):
        child = crossover(choose_parents(prob_list))
        mutate(child, prob_mutate)
        new_pop.append(child)
    return new_pop

        