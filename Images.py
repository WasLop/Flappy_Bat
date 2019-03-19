import pygame
from pygame.locals import *
from sys import exit
import time
from random import *

class image(object):
    def set_size(self,image,size):
        image = pygame.transform.scale(image, (size))
        return image
    def get_size (self,screen, div_w, div_h):

        whidth = screen.get_width()
        height = screen.get_height()
        whidth = int(whidth / div_w)
        height = int(height / div_h)

        return (whidth,height)

class background(image):
    def __init__(self):
        self.background1 = pygame.image.load("./images/background.png")

class player (image):
    def __init__(self):
        self.player_image = pygame.image.load("./images/bat1.png")
    def load_image(self,vercion):
        if (vercion == 1):
            self.player_image = pygame.image.load("./images/bat1.png")
        elif(vercion == 2):
            self.player_image = pygame.image.load("./images/bat2.png")
        elif(vercion == 3):
            self.player_image = pygame.image.load("./images/bat3.png")

class pipe (image):
    def __init__(self):
        self.pipe_img1 = pygame.image.load("./images/pipe1.png")
        self.pipe_img2 = pygame.image.load("./images/pipe1.png")
        self.pipe_img2 =  pygame.transform.flip(self.pipe_img2, 0, 180)

class pointer(image):
    def __init__(self):
        self.po_img = pygame.image.load("./images/pointer.png")
