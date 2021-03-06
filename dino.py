__author__ = "Shivam Shekhar"

import time
import os
import sys
import pygame
import random
from pygame import *
import neuralNet as nn

pygame.init()

#mexendo no movimento do dino
up = (1, 0)
down = (0, 1)
non = (0, 0)
restart = False

scr_size = (width,height) = (1200,150)
FPS = 60
gravity = 0.6

n_rex = 20
black = (0,0,0)
white = (255,255,255)
background_col = (235,235,235)

high_score = 0
last_score = []

screen = pygame.display.set_mode(scr_size)
clock = pygame.time.Clock()
pygame.display.set_caption("T-Rex Rush")

init_sound = pygame.mixer.Sound('Game/sprites/thank_you.wav')
jump_sound = pygame.mixer.Sound('Game/sprites/jump.wav')
die_sound = pygame.mixer.Sound('Game/sprites/doh1.wav')
die_sound_player = pygame.mixer.Sound('Game/sprites/ah_homer.wav')
checkPoint_sound1 = pygame.mixer.Sound('Game/sprites/Ooooh.wav')
checkPoint_sound2 = pygame.mixer.Sound('Game/sprites/woo.wav')
checkPoint_sound3 = pygame.mixer.Sound('Game/sprites/fuck_god.wav')
high_score_sound = pygame.mixer.Sound('Game/sprites/lick.wav')

def load_image(
    name,
    sizex=-1,
    sizey=-1,
    colorkey=None,
    ):

    fullname = os.path.join('Game/sprites', name)
    image = pygame.image.load(fullname)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)

    if sizex != -1 or sizey != -1:
        image = pygame.transform.scale(image, (sizex, sizey))

    return (image, image.get_rect())

def load_sprite_sheet(
        sheetname,
        nx,
        ny,
        scalex = -1,
        scaley = -1,
        colorkey = None,
        ):
    fullname = os.path.join('Game/sprites',sheetname)
    sheet = pygame.image.load(fullname)
    sheet = sheet.convert()

    sheet_rect = sheet.get_rect()

    sprites = []

    sizex = sheet_rect.width/nx
    sizey = sheet_rect.height/ny

    for i in range(0,ny):
        for j in range(0,nx):
            rect = pygame.Rect((j*sizex,i*sizey,sizex,sizey))
            image = pygame.Surface(rect.size)
            image = image.convert()
            image.blit(sheet,(0,0),rect)

            if colorkey is not None:
                if colorkey is -1:
                    colorkey = image.get_at((0,0))
                image.set_colorkey(colorkey,RLEACCEL)

            if scalex != -1 or scaley != -1:
                image = pygame.transform.scale(image,(scalex,scaley))

            sprites.append(image)

    sprite_rect = sprites[0].get_rect()

    return sprites,sprite_rect

def disp_gameOver_msg(retbutton_image,gameover_image):
    retbutton_rect = retbutton_image.get_rect()
    retbutton_rect.centerx = width / 2
    retbutton_rect.top = height*0.52

    gameover_rect = gameover_image.get_rect()
    gameover_rect.centerx = width / 2
    gameover_rect.centery = height*0.35

    screen.blit(retbutton_image, retbutton_rect)
    screen.blit(gameover_image, gameover_rect)

def extractDigits(number):
    if number > -1:
        digits = []
        i = 0
        while(number/10 != 0):
            digits.append(number%10)
            number = int(number/10)

        digits.append(number%10)
        for i in range(len(digits),5):
            digits.append(0)
        digits.reverse()
        return digits

class Dino():
    def __init__(self,sizex=-1,sizey=-1, p = False):
        if not p:
            self.images,self.rect = load_sprite_sheet('dino.png',5,1,sizex,sizey,-1)
            self.images1,self.rect1 = load_sprite_sheet('dino_ducking.png',2,1,59,sizey,-1)
        else: 
            self.images,self.rect = load_sprite_sheet('dino_p.png',5,1,sizex,sizey,-1)
            self.images1,self.rect1 = load_sprite_sheet('dino_ducking_p.png',2,1,59,sizey,-1)
        self.rect.bottom = int(0.98*height)
        self.rect.left = width/15
        self.image = self.images[0]
        self.index = 0
        self.counter = 0
        self.score = 0
        self.isJumping = False
        self.isDead = False
        self.isDucking = False
        self.isBlinking = False
        self.movement = [0,0]
        self.jumpSpeed = 11.5

        self.stand_pos_width = self.rect.width
        self.duck_pos_width = self.rect1.width

    def draw(self):
        screen.blit(self.image,self.rect)

    def checkbounds(self):
        if self.rect.bottom > int(0.98*height):
            self.rect.bottom = int(0.98*height)
            self.isJumping = False

    def update(self):
        if self.isJumping:
            #alterando a gravidade para quando a tecla precionada
            if pygame.key.get_pressed() == down:
                self.movement[1] = self.movement[1] + 3*gravity
            else:
                self.movement[1] = self.movement[1] + gravity

        if self.isJumping:
            self.index = 0
        elif self.isBlinking:
            if self.index == 0:
                if self.counter % 400 == 399:
                    self.index = (self.index + 1)%2
            else:
                if self.counter % 20 == 19:
                    self.index = (self.index + 1)%2

        elif self.isDucking:
            if self.counter % 5 == 0:
                self.index = (self.index + 1)%2
        else:
            if self.counter % 5 == 0:
                self.index = (self.index + 1)%2 + 2

        if self.isDead:
           self.index = 4

        if not self.isDucking:
            self.image = self.images[self.index]
            self.rect.width = self.stand_pos_width
        else:
            self.image = self.images1[(self.index)%2]
            self.rect.width = self.duck_pos_width

        self.rect = self.rect.move(self.movement)
        self.checkbounds()

        if not self.isDead and self.counter % 7 == 6 and self.isBlinking == False:
            self.score += 1
            if self.score == 100:
                if pygame.mixer.get_init() != None:
                    checkPoint_sound1.play()
            if self.score % 100 == 0 and self.score > 110 and self.score <390:
                if pygame.mixer.get_init() != None:
                    checkPoint_sound2.play()
            if self.score % 100 == 0 and self.score > 388:
                if pygame.mixer.get_init() != None:
                    checkPoint_sound3.play()

        self.counter = (self.counter + 1)

class Cactus(pygame.sprite.Sprite):
    def __init__(self,speed=5,sizex=-1,sizey=-1):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.images,self.rect = load_sprite_sheet('cacti-small.png',3,1,sizex,sizey,-1)
        self.rect.bottom = int(0.98*height)
        self.rect.left = width + self.rect.width
        self.image = self.images[random.randrange(0,3)]
        self.movement = [-1*speed,0]
        self.pos = self.rect.left 
    def draw(self):
        screen.blit(self.image,self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)

        if self.rect.right < 0:
            self.kill()

class Ptera(pygame.sprite.Sprite):
    def __init__(self,speed=5,sizex=-1,sizey=-1):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.images,self.rect = load_sprite_sheet('ptera.png',2,1,sizex,sizey,-1)
        self.ptera_height = [height*0.82,height*0.75,height*0.60]
        self.rect.centery = self.ptera_height[random.randrange(0,3)]
        self.rect.left = width + self.rect.width
        self.image = self.images[0]
        self.movement = [-1*speed,0]
        self.index = 0
        self.counter = 0

    def draw(self):
        screen.blit(self.image,self.rect)

    def update(self):
        if self.counter % 10 == 0:
            self.index = (self.index+1)%2
        self.image = self.images[self.index]
        self.rect = self.rect.move(self.movement)
        self.counter = (self.counter + 1)
        if self.rect.right < 0:
            self.kill()


class Ground():
    def __init__(self,speed=-5):
        self.image,self.rect = load_image('ground.png',-1,-1,-1)
        self.image1,self.rect1 = load_image('ground.png',-1,-1,-1)
        self.rect.bottom = height
        self.rect1.bottom = height
        self.rect1.left = self.rect.right
        self.speed = speed

    def draw(self):
        screen.blit(self.image,self.rect)
        screen.blit(self.image1,self.rect1)

    def update(self):
        self.rect.left += self.speed
        self.rect1.left += self.speed

        if self.rect.right < 0:
            self.rect.left = self.rect1.right

        if self.rect1.right < 0:
            self.rect1.left = self.rect.right

class Cloud(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image,self.rect = load_image('cloud.png',int(90*30/42),30,-1)
        self.speed = 1
        self.rect.left = x
        self.rect.top = y
        self.movement = [-1*self.speed,0]

    def draw(self):
        screen.blit(self.image,self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)
        if self.rect.right < 0:
            self.kill()

class Scoreboard():
    def __init__(self,x=-1,y=-1):
        self.score = 0
        self.tempimages,self.temprect = load_sprite_sheet('numbers.png',12,1,11,int(11*6/5),-1)
        self.image = pygame.Surface((55,int(11*6/5)))
        self.rect = self.image.get_rect()
        if x == -1:
            self.rect.left = width*0.89
        else:
            self.rect.left = x
        if y == -1:
            self.rect.top = height*0.1
        else:
            self.rect.top = y

    def draw(self):
        screen.blit(self.image,self.rect)

    def update(self,score):
        score_digits = extractDigits(score)
        self.image.fill(background_col)
        for s in score_digits:
            self.image.blit(self.tempimages[s],self.temprect)
            self.temprect.left += self.temprect.width
        self.temprect.left = 0


def introscreen():
    temp_dino = Dino(44,47)
    temp_dino.isBlinking = True
    gameStart = False

    callout,callout_rect = load_image('call_out.png',196,45,-1)
    callout_rect.left = width*0.05
    callout_rect.top = height*0.4

    temp_ground,temp_ground_rect = load_sprite_sheet('ground.png',15,1,-1,-1,-1)
    temp_ground_rect.left = width/20
    temp_ground_rect.bottom = height

    logo,logo_rect = load_image('logo.png',240,40,-1)
    logo_rect.centerx = width*0.6
    logo_rect.centery = height*0.6
    while not gameStart:
        if pygame.display.get_surface() == None:
            print("Couldn't load display surface")
            return True
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # temp_dino.isJumping = True
                        temp_dino.isBlinking = False
                        # temp_dino.movement[1] = -1*temp_dino.jumpSpeed

        temp_dino.update()

        if pygame.display.get_surface() != None:
            screen.fill(background_col)
            screen.blit(temp_ground[0],temp_ground_rect)
            if temp_dino.isBlinking:
                screen.blit(logo,logo_rect)
                screen.blit(callout,callout_rect)
            temp_dino.draw()

            pygame.display.update()

        clock.tick(FPS)
        if temp_dino.isJumping == False and temp_dino.isBlinking == False:
            gameStart = True


# Variáveis de jogo
redes = [nn.neuralNet(3, 1, [5]) for i in range(n_rex)]
dead = []
gamespeed = 12
gameOver = [False for n in range(n_rex)]
p_gameOver = False
playerDino = [Dino(44,47) for n in range(n_rex)]
player = (Dino(44,47, True))
keys = [non for n in range(n_rex)]



cacti = pygame.sprite.Group()
pteras = pygame.sprite.Group()
clouds = pygame.sprite.Group()
last_obstacle = pygame.sprite.Group()

dists = []
heights = []

def gameplay():
    global redes
    global dead
    global n_rex
    global high_score
    global last_score
    global gamespeed
    global keys
    global restart
    gamespeed = 7
    global gameOver
    gameOver = [False for n in range(n_rex)]
    global playerDino
    playerDino = [Dino(44,47) for n in range(n_rex)]
    global player
    global p_gameOver
    player = (Dino(44,47, True))
    keys = [non for n in range(n_rex)]
    startMenu = False
    gameQuit = False
    new_ground = Ground(-1*gamespeed)
    scb = Scoreboard()
    highsc = Scoreboard(width*0.78)
    counter = 0

    global cacti 
    cacti = pygame.sprite.Group()
    global pteras
    pteras = pygame.sprite.Group()
    global clouds
    clouds = pygame.sprite.Group()
    global last_obstacle
    last_obstacle = pygame.sprite.Group()

    global dists
    global heights

    Cactus.containers = cacti
    Ptera.containers = pteras
    Cloud.containers = clouds

    retbutton_image,retbutton_rect = load_image('replay_button.png',35,31,-1)
    gameover_image,gameover_rect = load_image('game_over.png',190,11,-1)

    temp_images,temp_rect = load_sprite_sheet('numbers.png',12,1,11,int(11*6/5),-1)
    HI_image = pygame.Surface((22,int(11*6/5)))
    HI_rect = HI_image.get_rect()
    HI_image.fill(background_col)
    HI_image.blit(temp_images[10],temp_rect)
    temp_rect.left += temp_rect.width
    HI_image.blit(temp_images[11],temp_rect)
    HI_rect.top = height*0.1
    HI_rect.left = width*0.73

    while not gameQuit:
        while startMenu:
            pass
        while playerDino:
            dists = [] 
            heights = []

            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
                gameQuit = True
                gameOver = [True for n in range(n_rex)]
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameQuit = True
                        gameOver = [True for n in range(n_rex)]





            #controlando o dino player
            p_keys = pygame.key.get_pressed()     
            if not p_gameOver:
                if not player.isJumping:
                    if p_keys[pygame.K_UP]:
                        if (player.rect.bottom == int(0.98*height)): 
                            player.isJumping = True
                            if pygame.mixer.get_init() != None:
                                jump_sound.play()
                            player.movement[1] = -1*player.jumpSpeed

                    if p_keys[pygame.K_DOWN]: 
                        if not (player.isDead):
                            player.isDucking = True
                    else:
                        player.isDucking = False
                    
            # controlando o dino da rede
            for j, rex in enumerate(playerDino):
                if not rex.isJumping:
                    if keys[j] == up:
                        if (rex.rect.bottom == int(0.98*height)): 
                            rex.isJumping = True
                            if pygame.mixer.get_init() != None:
                                jump_sound.play()
                            rex.movement[1] = -1*rex.jumpSpeed

                    if keys[j] == down: 
                        if not (rex.isDead): 
                            rex.isDucking = True
                    else:
                        rex.isDucking = False





            #Verificando colisão com o dino player
            if not p_gameOver:
                for c in cacti:
                    c.movement[0] = -1*gamespeed
                    if pygame.sprite.collide_mask(player,c):
                        player.isDead = True
                    dists.append(c.rect.left - rex.rect.right)
                    heights.append(c.rect.centery)

                for p in pteras:
                    p.movement[0] = -1*gamespeed
                    if pygame.sprite.collide_mask(player,p):
                        player.isDead = True
                    dists.append(p.rect.left - rex.rect.right)
                    heights.append(p.rect.centery)

            #Verificando colisão com os dinos da rede
            for c in cacti:
                for rex in playerDino:
                    c.movement[0] = -1*gamespeed
                    if pygame.sprite.collide_mask(rex,c):
                        rex.isDead = True
                dists.append(c.rect.left - rex.rect.right)
                heights.append(c.rect.centery)

            for p in pteras:
                for rex in playerDino:
                    p.movement[0] = -1*gamespeed
                    if pygame.sprite.collide_mask(rex,p):
                        rex.isDead = True
                dists.append(p.rect.left - rex.rect.right)
                heights.append(p.rect.centery)




            #Gerando obstaculos e nuvens
            if len(cacti) < 2:
                if len(cacti) == 0:
                    last_obstacle.empty()
                    last_obstacle.add(Cactus(gamespeed,40,40))
                else:
                    for l in last_obstacle:
                        if l.rect.right < width*0.4 and random.randrange(0,50) == 10:
                            last_obstacle.empty()
                            last_obstacle.add(Cactus(gamespeed, 40, 40))

            if len(pteras) == 0 and random.randrange(0,150) < 2 and counter > 200:
                for l in last_obstacle:
                    if l.rect.right < width*0.4:
                        last_obstacle.empty()
                        last_obstacle.add(Ptera(gamespeed, 46, 40))

            if len(clouds) < 5 and random.randrange(0,300) == 10:
                Cloud(width,random.randrange(height/5,height/2))




            for rex in playerDino:
                rex.update()
            if not p_gameOver:
                player.update()
                scb.update(player.score)
            cacti.update()
            pteras.update()
            clouds.update()
            new_ground.update()
            for rex in playerDino:
                scb.update(rex.score)
            highsc.update(high_score)

            if pygame.display.get_surface() != None:
                screen.fill(background_col)
                new_ground.draw()
                clouds.draw(screen)
                scb.draw()
                if high_score != 0:
                    highsc.draw()
                    screen.blit(HI_image,HI_rect)
                cacti.draw(screen)
                pteras.draw(screen)
                for rex in playerDino:
                    rex.draw()
                if not p_gameOver:
                    player.draw()
                pygame.display.update()
            clock.tick(FPS)
            



            #Verificando mortes dos dinos da rede
            if not p_gameOver:
                if player.isDead:
                        p_gameOver = True
                        del(player)
                        die_sound_player.play()

            #Verificando mortes dos dinos da rede
            for i, rex in enumerate(playerDino):
                if rex.isDead:
                    gameOver[i] = True
                    last_score.append(rex.score)
                    del(playerDino[i])
                    del(keys[i])
                    dead.append(redes[i])
                    del(redes[i])
                    if pygame.mixer.get_init() != None:
                            die_sound.play()
                    if rex.score > high_score:
                        high_score = rex.score
                        if not playerDino:
                            high_score_sound.play()
            



            if counter%700 == 699:
                new_ground.speed -= 1
                gamespeed += 1

            counter = (counter + 1)

        if gameQuit:
            break

        while not playerDino or p_gameOver:
            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
                gameQuit = True
                gameOver = False
                p_gameOver = False
            else:
               for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameQuit = True
                        gameOver = False
                        p_gameOver = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            gameQuit = True
                            gameOver = False
                            p_gameOver = False
                        if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            gameOver = False
                            p_gameOver = False
                            gameplay()
               highsc.update(high_score)
            if pygame.display.get_surface() != None:
                disp_gameOver_msg(retbutton_image,gameover_image)
                if high_score != 0:
                    highsc.draw()
                    screen.blit(HI_image,HI_rect)
                pygame.display.update()
            clock.tick(FPS)
            #Reiniciar o jogo automaticamente
            if restart:
                gameOver = False
                p_gameOver = False
                last_score = []
                dead = []
                restart = False
                gameplay()

    pygame.quit()
    quit()

def play():
    if pygame.mixer.get_init() != None:
        init_sound.play()
    isGameQuit = introscreen()
    if not isGameQuit:
        gameplay()
# play()
