import pygame
import math
import config as cfg
pygame.init()

animate_flag = True

screen_size = screen_width, screen_height = 500, 500

screen = pygame.display.set_mode(screen_size)
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((255, 255, 255))

hosts = pygame.sprite.Group()
speakers = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

origin = [
    screen_width/2,
    screen_height/2
]


def reset():
    global hosts, speakers, all_sprites
    hosts = pygame.sprite.Group()
    speakers = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()


class Host(pygame.sprite.Sprite):
    def __init__(self, color, x=origin[0], y=origin[1]):
        pygame.sprite.Sprite.__init__(self)

        self.species_size = self.species_width, self.species_height = 20, 20
        self.size = self.width, self.height = self.species_width, self.species_height
        self.color = color
        self.image = pygame.Surface(self.size)
        self.image.fill(self.color)
        self.x = x
        self.y = y

        self.rect = self.image.get_rect()
        self.area = screen.get_rect()
        self.rect.left = x - self.width / 2
        self.rect.top = y - self.height / 2
        self.add(hosts)
        self.add(all_sprites)

        self.ear1 = {
            "x": x - self.width / 2,
            "y": y
        }

        self.ear2 = {
            "x": x + self.width / 2,
            "y": y
        }


speaker_width = 5
speaker_height = 5


class Speaker(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([speaker_width, speaker_height])
        self.image.fill((0, 200, 0))
        self.x = x
        self.y = y
        self.intensity = 1e8
        self.velocity = 10

        self.rect = self.image.get_rect()
        self.area = screen.get_rect()
        self.rect.top = self.y - speaker_height / 2
        self.rect.left = self.x - speaker_width / 2

        self.add(speakers)
        self.add(all_sprites)


def draw_response(response, surface):
    angle = cfg.to_deg(response[1], response[0])
    angle = math.radians(angle)
    end_pos = [
        origin[0] + math.cos(angle)*screen_width,
        origin[1] - math.sin(angle)*screen_width
    ]
    pygame.draw.line(surface, (200, 0, 0), origin, end_pos)
    print("END POS")
    print(end_pos)


def draw_answer(speaker_pos, surface):
    end_pos = [
        speaker_pos[0],
        speaker_pos[1]
    ]
    pygame.draw.line(surface, (0, 200, 0), origin, end_pos)