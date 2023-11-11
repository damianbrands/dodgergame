import random
import pygame
from pygame.sprite import *
from sys import exit

dimensionX = 800
dimensionY = 800

virusScale = 10

background = pygame.image.load('assets/background.png')
background = pygame.transform.scale(background, (dimensionX, dimensionY))

points = 0


class Virus(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.x = random.randint(0, dimensionX)
        self.y = -75
        self.image = pygame.transform.scale(pygame.image.load('assets/virus{}.png'.format(random.randint(0, 3))),
                                            (dimensionX / virusScale, dimensionY / virusScale))
        self.rect = self.image.get_rect()
        self.speed = 5
        self.angle = random.randint(-1, 1)

    def update(self):
        self.y += self.speed
        self.x += self.angle
        if dimensionY + 75 < self.y:
            self.y = -75
            self.x = random.randint(0, dimensionX)
            if self.speed < 13:
                self.speed += 1

        self.rect.y = self.y
        self.rect.x = self.x


pygame.init()
sprites = Group()
virus = Virus()

sprites.add(virus)

screen = pygame.display.set_mode((dimensionX, dimensionY))
pygame.display.set_caption('Dodger')
clock = pygame.time.Clock()

counter, text = 0, '0'.rjust(3)
pygame.time.set_timer(pygame.USEREVENT, 1000)
font = pygame.font.SysFont('Arial', 30)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.USEREVENT:
            counter += 1
            text = str(counter).rjust(3)
            newVirus = Virus()
            sprites.add(newVirus)

    screen.blit(background, (0, 0))
    sprites.update()
    sprites.draw(screen)
    screen.blit(font.render(text, True, (0, 0, 0)), (0, 0))
    pygame.display.update()
    clock.tick(60)
