import pygame

class sound(object):
    def play(self,sound):
        pygame.mixer.init()
        pygame.mixer.music.load("./music/"+sound)
        pygame.mixer.music.play()

        pygame.event.wait()

