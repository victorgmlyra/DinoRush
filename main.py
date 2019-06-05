from numpy import random
import threading
import time
import dino
import neuralNet as nn
import heritage 
# dino.dists = lista com a distancia de todos os obstaculos em relação ao dino
# dino.heights = lista com a altura de todos os obstaculos na tela
# dino.gamespeed = velocidade do jogo


th = threading.Thread(target = dino.play) 
th.start()
x=1


while True:
    params = list(zip(dino.heights, dino.dists))
    params = sorted(params, key=lambda x: x[1])
    height = 0
    dist = 600
    for param in params:
        if param[1] >= 0:
            height = param[0]
            dist = param[1]
            break

    for n in range(len(dino.playerDino)):
        input_params = [height, dist, dino.gamespeed]
        if n < len(dino.playerDino):
            out = dino.redes[n].run(input_params)
            if out > 0.4 and n < len(dino.keys): 
                dino.keys[n] = dino.up
            elif out < -0.4 and n < len(dino.keys):
                dino.keys[n] = dino.down
            else:
                if n < len(dino.keys):
                    dino.keys[n] = dino.non
    if not dino.playerDino:
        time.sleep(0.3) 
        pop = list(zip(dino.dead, dino.last_score))
        dino.redes = heritage.create_new_population(pop) 
        time.sleep(1.5) 
        dino.restart = True
        time.sleep(0.8) 
    
        
th.join()