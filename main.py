import threading
import dino

# dino.dists = lista com a distancia de todos os obstaculos em relação ao dino
# dino.heights = lista com a altura de todos os obstaculos na tela
# dino.gamespeed = velocidade do jogo
th = threading.Thread(target = dino.play) 
th.start()

while True:
    print(dino.dists, "  ", dino.heights)

th.join()