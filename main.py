# Referencia: https://www.edureka.co/blog/snake-game-with-pygame/
# Raul Jimenez
# Bryann Alfaro
# Donaldo Garcia
# Oscar Saravia
# Proyecto de IA

import time
import pygame
import random
from sys import exit

pygame.init()
width = 70
height = 70
posx = random.randint(0, width-1)
posy = random.randint(0, height-1)

screen = pygame.display.set_mode((width*10, height*10))
screen2 = pygame.Surface((width, height))

myfont = pygame.font.SysFont('Comic Sans MS', 10)
myfont2 = pygame.font.SysFont('Comic Sans MS', 9)

pygame.display.set_caption('SNAKE GAME')
pygame.display.set_icon(pygame.image.load('snake.jpg'))


game = True
snake_list = []

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)
white = (255, 255, 255)


def Your_score(score):
    value = score_font.render("Puntuacion: " + str(score), True, white)
    screen.blit(value, [0, 0])


def draw_food(posx, posy):
    food_x = random.randint(0, width-1)
    food_y = random.randint(0, height-1)

    if food_x == posx:
        food_x += 1
    if food_y == posy:
        food_y += 1

    return food_x, food_y


def draw_snake(snake_list):
    for pos in snake_list:
        pygame.draw.rect(screen2, (254, 253, 22), (pos[0], pos[1], 1, 1))


food_x, food_y = draw_food(posx, posy)
snake_len = 1
x_delta = 0
y_delta = 0


class button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2, self.y -
                             2, self.width+4, self.height+4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y,
                         self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2),
                     self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


quitButton = button((0, 255, 230), 100, 400, 250, 100, 'Quit')
continueButton = button((0, 255, 230), 400, 400, 250, 100, 'Play')
play = True
sonido_fondo = pygame.mixer.Sound("sound.mp3")
pygame.mixer.Sound.play(sonido_fondo, -1)
bandera_sound = True
while play:

    while game:

        screen.fill((0, 0, 0))
        screen.blit(pygame.transform.scale(
            screen2, screen.get_rect().size), (0, 0))
        Your_score(snake_len - 1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    x_delta = 0
                    y_delta = -1
                if event.key == pygame.K_DOWN:
                    y_delta = 1
                    x_delta = 0
                if event.key == pygame.K_LEFT:
                    x_delta = -1
                    y_delta = 0
                if event.key == pygame.K_RIGHT:
                    x_delta = 1
                    y_delta = 0
        posx += x_delta
        posy += y_delta
        screen2.fill((0, 0, 0))

        # Si toca bordes
        if(posx == width):
            game = False
        if(posy == height):
            game = False
        if(posx == -1):
            game = False
        if(posy == -1):
            game = False
        pygame.draw.rect(screen2, (24, 53, 225), (food_x, food_y, 1, 1))

        snake_Head = [posx, posy]
        snake_list.append(snake_Head)
        # Mantener las referencias de cada posicion de la snake actualizada
        if len(snake_list) > snake_len:
            del snake_list[0]

        # Si la snake toca a si misma
        for x in snake_list[:-1]:
            if x == snake_Head:
                game = False

        # Se revisa que el tamaño de la serpiente mas la nueva fruta no sea mayor al tamaño de la pantalla
        if snake_len + 1 >= (width*height):
            game = False
        # Se dibuja en cada ciclo
        draw_snake(snake_list)

        # Si la snake come alimento
        if posx == food_x and posy == food_y:
            food_x, food_y = draw_food(posx, posy)
            snake_len += 1
            Your_score(snake_len - 1)
        pygame.display.update()
        pygame.time.Clock().tick(10)

    # Si pierde
    screen.blit(pygame.transform.scale(
        screen2, screen.get_rect().size), (0, 0))
    screen.fill((0, 255, 0))
    screen.blit(pygame.font.SysFont(None, 50).render(
        'YOU LOST', True, (255, 0, 0)), [(width*7)//2, (height*9)//2])

    continueButton.draw(screen, (0, 0, 0))
    quitButton.draw(screen, (0, 0, 0))
    pygame.mixer.pause()
    pygame.display.update()
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if quitButton.isOver(pos):
                play = False
                pygame.mixer.pause()
            if continueButton.isOver(pos):
                posx = random.randint(0, width-1)
                posy = random.randint(0, height-1)
                snake_len = 1
                snake_list = []
                game = True
                pygame.mixer.pause()
                pygame.mixer.Sound.play(sonido_fondo, -1)

pygame.quit()
