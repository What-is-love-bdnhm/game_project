from player import Player
from sprites import *
from ray_casting import ray_casting_walls
from drawing import Drawing
from interaction import Interaction

# запуск pygame + создание основного окна и окна для миникарты
pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
sc_map = pygame.Surface(MINIMAP_RES)

# запуск основных функций
sprites = Sprites()
clock = pygame.time.Clock()
player = Player(sprites)
drawing = Drawing(sc, sc_map, player, clock)
interaction = Interaction(player, sprites, drawing)

# отрисовка меню
drawing.menu()
# невидимость курсора в окне
pygame.mouse.set_visible(False)
# запуск музыки
interaction.play_music()

while True:
    player.movement()  # анализ нажатия клавиш
    drawing.background(player.angle)  # отрисовка неба и пола
    walls, wall_shot = ray_casting_walls(player, drawing.textures)  # улавливание стен лучами
    drawing.world(walls + [obj.object_locate(player) for obj in sprites.list_of_objects])  # отрисовка мира
    drawing.fps(clock)  # счетчик фпс
    drawing.mini_map(player)  # миникарта
    drawing.player_weapon([wall_shot, sprites.sprite_shot])  # отрисовка оружия

    interaction.interaction_objects()
    interaction.npc_action()  # анализ действия нпс. на данный момент бесполезно без ии
    interaction.clear_world()  # удаление мертвых объектов из списка для анализа

    pygame.draw.circle(sc, (0, 255, 0), (HALF_WIDTH, HALF_HEIGHT), 5, 1)  # прицел

    interaction.check_win()



    pygame.display.flip()
    clock.tick(FPS)

