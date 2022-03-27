import time
import pygame
import random
from sys import exit

pygame.init()
width = 70
height = 70
posx = random.randint(0,width-1)
posy = random.randint(0,height-1)
screen = pygame.display.set_mode((width*10, height*10))
screen2  = pygame.Surface((width, height))

myfont = pygame.font.SysFont('Comic Sans MS', 10)
myfont2 = pygame.font.SysFont('Comic Sans MS', 9)

pygame.display.set_caption('SNAKE GAME')
pygame.display.set_icon(pygame.image.load('snake.jpg'))

pygame.draw.rect(screen2, (254,253,225), (posx, posy, 1, 1))
game = True
while game:
  screen.blit(pygame.transform.scale(screen2, screen.get_rect().size), (0, 0))
  for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        exit()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
             posy -=1
        if event.key == pygame.K_DOWN:
                posy +=1
        if event.key == pygame.K_LEFT:
                posx -=1
        if event.key == pygame.K_RIGHT:
                posx +=1

  screen2.fill((0,0,0))
  if(posx==width):
      game = False
  if(posy==height):
        game = False
  if(posx==-1):
       game = False
  if(posy==-1):
        game = False
  pygame.draw.rect(screen2, (254,253,225), (posx, posy, 1, 1))
  pygame.time.Clock().tick(30)
  pygame.display.update()

screen.blit(pygame.transform.scale(screen2, screen.get_rect().size), (0, 0))
screen.fill((0,255,0))
screen.blit(pygame.font.SysFont(None, 50).render('YOU LOST', True, (255,0,0)), [(width*7)//2, (height*9)//2])
pygame.display.update()
time.sleep(2)

pygame.quit()