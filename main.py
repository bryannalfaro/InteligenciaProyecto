import pygame
import random
from sys import exit

pygame.init()
width = 300
height = 300
screen = pygame.display.set_mode((width, height))

myfont = pygame.font.SysFont('Comic Sans MS', 10)
myfont2 = pygame.font.SysFont('Comic Sans MS', 9)

pygame.display.set_caption('SNAKE GAME')
pygame.display.set_icon(pygame.image.load('snake.jpg'))

while True:
  for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        exit()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
             print('up')

        if event.key == pygame.K_DOWN:
             print('down')


  pygame.display.flip()