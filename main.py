import random
import pygame
from pygame.sprite import Sprite, Group
from sys import exit

# Constants
DIMENSION_X = 800
DIMENSION_Y = 800
VIRUS_SCALE = 10

# Initialize Pygame
pygame.init()

# Load Background
background = pygame.image.load('assets/background.png')
background = pygame.transform.scale(background, (DIMENSION_X, DIMENSION_Y))


# Player class
class Player(Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('assets/player.png'),
                                            (DIMENSION_X // VIRUS_SCALE / 2, DIMENSION_Y // VIRUS_SCALE / 2))
        self.rect = self.image.get_rect()
        self.rect.centerx = DIMENSION_X // 2
        self.rect.centery = DIMENSION_Y // 2


# Virus class
class Virus(Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load('assets/virus{}.png'.format(random.randint(0, 3))),
            (DIMENSION_X // VIRUS_SCALE, DIMENSION_Y // VIRUS_SCALE)
        )
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, DIMENSION_X)
        self.rect.y = -self.rect.height
        self.speed = 1
        self.angle = random.randint(-1, 1)

    def update(self):
        self.rect.y += self.speed
        self.rect.x += self.angle
        if self.rect.y > DIMENSION_Y:
            self.reset()

    def reset(self):
        self.rect.y = -self.rect.height
        self.rect.x = random.randint(0, DIMENSION_X)
        if self.speed < 10:
            self.speed += 1


# Game class
class DodgerGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((DIMENSION_X, DIMENSION_Y))
        pygame.display.set_caption('Dodger')
        self.clock = pygame.time.Clock()
        self.sprites = Group()
        self.player = Player()
        self.sprites.add(self.player)
        self.viruses = Group()
        self.score = 0
        self.font = pygame.font.SysFont('Arial', 30)
        self.virus_spawn_threshold = 100

    def run(self):
        pygame.time.set_timer(pygame.USEREVENT + 1, 1000)
        pygame.time.set_timer(pygame.USEREVENT + 2, 10000)
        self.spawn_virus()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.USEREVENT + 1:
                    self.score += 1
                if event.type == pygame.USEREVENT + 2:
                    self.spawn_virus()
                    if self.score % self.virus_spawn_threshold == 0:
                        self.spawn_virus()

            self.screen.blit(background, (0, 0))
            self.handle_input()
            self.sprites.update()
            self.check_collisions()
            self.sprites.draw(self.screen)
            self.display_score()

            pygame.display.update()
            self.clock.tick(60)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.player.rect.left > 0:
            self.player.rect.x -= 5
        if keys[pygame.K_RIGHT] and self.player.rect.right < DIMENSION_X:
            self.player.rect.x += 5
        if keys[pygame.K_UP] and self.player.rect.top > 0:
            self.player.rect.y -= 5
        if keys[pygame.K_DOWN] and self.player.rect.bottom < DIMENSION_Y:
            self.player.rect.y += 5

    def spawn_virus(self):
        virus = Virus()
        self.sprites.add(virus)
        self.viruses.add(virus)

    def check_collisions(self):
        collisions = pygame.sprite.spritecollide(self.player, self.viruses, True)
        if collisions:
            self.reset_game()

    def reset_game(self):
        self.sprites.empty()
        self.viruses.empty()
        self.sprites.add(self.player)
        self.spawn_virus()
        self.score = 0
        self.player.rect.centerx = DIMENSION_X // 2
        self.player.rect.centery = DIMENSION_Y // 2

    def display_score(self):
        score_text = str(self.score).rjust(3)
        self.screen.blit(self.font.render(score_text, True, (0, 0, 0)), (0, 0))


if __name__ == "__main__":
    game = DodgerGame()
    game.run()
