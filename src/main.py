import pygame
from settings import *
from player import Player
import math
from map import world_map
from ray_casting import ray_casting

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
player = Player()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    player.movement()
    screen.fill(BLACK)

    pygame.draw.rect(screen, BLUE, (0,0, WIDTH, HALF_HEIGHT))
    pygame.draw.rect(screen, DARKGRAY, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))

    ray_casting(screen, player.pos(), player.angle)

    # pygame.draw.circle(screen, GREEN, (int(player.x), int(player.y)), 12)
    # pygame.draw.line(screen, GREEN, player.pos(), (player.x + WIDTH * math.cos(player.angle),
    #                                                player.y + WIDTH * math.sin(player.angle)))
    # for x, y in world_map:
    #     pygame.draw.rect(screen, DARKGRAY, (x, y, TILE, TILE), 5)

    pygame.display.flip()
    clock.tick(FPS)
