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
#th1 = threading.Thread(target = dino.play) 
#th1.start()

while True:
    dino.keys = dino.up if x%2==0 else dino.down
    time.sleep(random.random())
    print(dino.dists, dino.heights, dino.gamespeed, dino.keys)
    x+=1
    while dino.gameOver == True:
        time.sleep(0.3)
        dino.keys = dino.restart
        
        
th.join()