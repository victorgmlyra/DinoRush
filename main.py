import threading
import dino
import time
from numpy import random

# dino.dists = lista com a distancia de todos os obstaculos em relação ao dino
# dino.heights = lista com a altura de todos os obstaculos na tela
# dino.gamespeed = velocidade do jogo


th = threading.Thread(target = dino.play) 
th.start()
x=1


while True:
    
    for n in range(len(dino.keys)):
        if n < len(dino.keys):
            dino.keys[n] = dino.up if x%2==0 else dino.down
            time.sleep(random.random()/20)
        x+=1
    while not dino.playerDino:
        time.sleep(0.3) 
        dino.restart = True
        print('\n', dino.last_score, '\n')
        time.sleep(0.8) 
    
        
th.join()