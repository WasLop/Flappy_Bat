import pygame
import  Game
from pygame.locals import *
from sys import exit
import time
from random import *

pygame.init()
pygame.mixer.init()
options = Game.options()
screen = pygame.display.set_mode(options.size, 0, 32)
mn = True
name = ""
while True:
    play = Game.play(screen)
    game_over = Game.game_over(screen)
    menu = Game.menu(screen)
    records = Game.records(screen)

    if mn:
        menu.loop_menu(records)
        records.start()
    else:
        records.name = name
    play.main_loop()
    mn, name = game_over.lopp_game_over(play.score,records.name,records)
