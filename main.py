__author__ = 'Nathaniel'
import pygame, sys

pygame.init()

screen=pygame.display.set_mode((1024,568))
pygame.display.set_caption("Fireworks with a beat?")
gameActive = 1

divider = pygame.image.load("./divider.png")
loadButton = pygame.image.load("./load.gif")

background = pygame.Surface((1024,568))
background = background.convert()
background.fill((100, 100, 255))

screen.blit(background, (0, 0))
screen.blit(divider,(250,0))
screen.blit(loadButton,(10,60))

pygame.display.flip()

#loadButton.
while gameActive:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        gameActive=0
    pygame.display.flip()