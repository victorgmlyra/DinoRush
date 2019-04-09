import pygame

pygame.init()

scrrenWidht = 1300
screenHeight = 450

window = pygame.display.set_mode((scrrenWidht, screenHeight))
pygame.display.set_caption('Dino Rush!!')

widht = 70
height = 100
x = widht
y = screenHeight - height
vel = 10

isJump = False
jumpCount = 11
lower = 1
lowerSpace = 0
run = True
while run:
    pygame.time.delay(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if not isJump:
        if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
            isJump = True
        if keys[pygame.K_DOWN]:
            lower = 2
            lowerSpace = 1
        else:
            lower = 1
            lowerSpace = 0
    else:
        if jumpCount >= -11:
            neg = 1
            if jumpCount < 0:
                neg = -1
            y -= (jumpCount ** 2) * 0.5 * neg
            jumpCount -= 1
        else:
            isJump = False
            jumpCount = 11

    window.fill((255, 255, 255))
    pygame.draw.rect(window, (0, 0, 0), (x, y + lowerSpace * height / 2, widht, height / lower))
    pygame.display.update()

pygame.quit()