import sys
import pygame
import random

pygame.init()

screen = pygame.display.set_mode((0, 0),pygame.FULLSCREEN)

sprite = pygame.image.load("ship.bmp")

pygame.display.set_caption("My Pygame")
up = down = left = right = x = y = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                sys.exit()
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                left = True
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                right = True
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                up = True
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                down = True
            elif event.key == pygame.K_r:
                screen.fill((230, 230, 230))
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    left = False
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                right = False
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                up = False
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                down = False

    if left:
        x -= 1
    if right:
        x += 1
    if up:
        y -= 1
    if down:
        y += 1

    screen.blit(sprite, (x, y))
    r = random.randint(1, 255)
    g = random.randint(1, 255)
    b = random.randint(1, 255)

    rect = pygame.Rect(x, y, 120, 120)
    #pygame.draw.rect(screen, (r, g, b), rect, 0)
    pygame.display.flip()
    screen.fill((230, 230, 230))

