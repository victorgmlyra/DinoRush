from numpy import random
import threading
import time, keyboard
import dino
import neuralNet as nn
import heritage 
# dino.dists = lista com a distancia de todos os obstaculos em relação ao dino
# dino.heights = lista com a altura de todos os obstaculos na tela
# dino.gamespeed = velocidade do jogo

gen = 1
th = threading.Thread(target = dino.play) 
th.start()

print('Generation: ', gen)
while True:
    params = sorted(zip(dino.heights, dino.dists)), key=lambda x: x[1])
    params = [h, d for h, d in params if d >= 0]
    height, dist = params[0] if params else 127, 600

    for n, _ in enumerate(dino.playerDino):
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
        gen +=1
        time.sleep(0.3) 
        pop = list(zip(dino.dead, dino.last_score))
        dino.redes = heritage.create_new_population(pop) 
        time.sleep(1.5) 
        dino.restart = True
        print('Generation: ', gen)
        time.sleep(0.8) 
    
        
th.join()