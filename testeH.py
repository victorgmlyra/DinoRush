import neuralNet as nn
import numpy as np
import heritage
import random

redes = [nn.neuralNet(2, 2, [2]) for i in range(3)]
fits = [46, 162, 208]
zipado = list(zip(redes, fits))
pop = heritage.create_new_population(zipado)
print([r.network for r in redes])
print('\n pop \n')
print([p.network for p in pop])
# oi = heritage.create_probablity_list(zipado)


# oi = heritage.crossover(redes)
# print(oi.network)
# heritage.mutate(oi, 0.2)
# print()
# print(oi.network)
