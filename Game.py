import pygame
import Images
from pygame.locals import *
from sys import exit
import pickle
import Player
from random import *

class play(object):
    def __init__(self, screen):
        self.options = options()
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.backgrounds = Images.background()
        self.backgrounds.background1 = self.backgrounds.set_size(self.backgrounds.background1,
                                                                 (5000, self.screen.get_height()))
        self.events = events()
        self.x_city = 0
        self.player = player(self.screen)
        self.pipe = pipe()
        self.loop = True
        self.score = score()
    def main_loop(self):
        while self.loop:
            ev = self.events.event()

            self.player.flay(ev,self.clock)
            self.loop = self.pipe.colision(self.player, self.score)

            self.screen.blit(self.backgrounds.background1,(self.x_city,0))
            self.screen.blit(self.player.img.player_image,self.player.pos)
            self.screen.blit(self.pipe.img.pipe_img1,self.pipe.pos1)
            self.screen.blit(self.pipe.img.pipe_img2, self.pipe.pos2)
            self.score.print_score(self.screen,(300,10))
            self.pipe.move()

            self.x_city -= 0.5
            if self.x_city < -1650:
                self.x_city = 0
            pygame.display.update()

class events(object):
    def event(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    return "up"
                elif event.key == K_DOWN:
                    return "down"
                elif event.key == K_LEFT:
                    return "left"
                elif event.key == K_RIGHT:
                    return "right"
                elif event.key == K_SPACE:
                    return "space"
                elif event.key == K_ESCAPE:
                    return "esc"
                elif event.key == K_RETURN:
                    return "enter"
                elif event.key == K_BACKSPACE:
                    return "b_space"
                else:
                    return event.unicode
            elif event.type == MOUSEBUTTONDOWN:
                return "space"
            elif event.type == KEYUP:
                return "off"
        return ""

class options (object):
    def __init__(self):
        self.size = (640,480)

class player(object):
    def __init__(self,screen):
        self.img = Images.player()
        self.size_player = self.img.get_size(screen, 13, 10)
        self.img.player_image = self.img.set_size(self.img.player_image, self.size_player)
        self.pos = (screen.get_width()/2 - 100,screen.get_height()/2)
        self.speed = 20
        self.fl = False
        self.pos_max = self.pos[1] - 80

    def flay(self,event,clock):
        time_passed = clock.tick(30)
        time_passed_seconds = time_passed / 1000.0
        distance = time_passed_seconds + self.speed
        x, y = self.pos

        if event == "space":
            self.speed = 25
            pygame.mixer.init()
            pygame.mixer.music.load("./music/hit.mp3")
            pygame.mixer.music.play()
            self.pos_max = y - 180
            self.img.load_image(3)
            self.img.player_image = self.img.set_size(self.img.player_image, self.size_player)
            self.fl = True
        elif self.pos[1] <= self.pos_max or y < -40:
            self.img.load_image(1)
            self.img.player_image = self.img.set_size(self.img.player_image, self.size_player)
            self.speed = 0
            self.fl = False
        if self.fl:
            if self.speed > 2:
                self.speed -= 1.8;
            if self.speed < 20:
                self.img.load_image(2)
                self.img.player_image = self.img.set_size(self.img.player_image, self.size_player)
            y -= distance
        else:

            if self.speed < 25:
                self.speed += 3
            if y < 430:
                y += distance

        self.pos = x,y

class pipe (object):
    def __init__(self):
        self.img = Images.pipe()
        self.img.pipe_img1 = self.img.set_size(self.img.pipe_img1, (80,400))
        self.img.pipe_img2 = self.img.set_size(self.img.pipe_img2, (80, 400))
        self.pos1 = (1500, 320)
        self.pos2 = (1500,-250)
    def move (self):
        x,y1 = self.pos1
        y2 = self.pos2[1]
        x -= 8
        if x < - 50:
            x = 640
            perc = randint(0, 100)

            if perc <= 30:
                y1 = 220
                y2 = - 350
            elif 30 < perc <= 60:
                y1 = 420
                y2 = - 150
            else:
                y1 = 320
                y2 = -250


        self.pos1 = x, y1
        self.pos2 = x, y2

    def colision (self, player,score):


        if  self.pos1[0] + 80 > player.pos[0] + 30> self.pos1[0]:
            if player.pos[1] < self.pos2[1] + 385 or player.pos[1] + 13 > self.pos1[1]:
                pygame.mixer.music.load("./music/collision.mp3")
                pygame.mixer.music.play()
                return False
            score.help_score = True
        else:
            if score.help_score:
                score.score += 1
                score.help_score = False

        return True

class score(object):
    def __init__(self):
        self.score = 0
        self.help_score = False
        self.myfont = pygame.font.SysFont("Rosewood Std Regular", 70)

    def print_score(self, screen, pos):
        label = self.myfont.render(str(self.score), 1, (0, 0, 0))
        screen.blit(label,(pos))

class game_over (object):
    def __init__(self,screen):
        self.screen = screen
        self.myfont1 = pygame.font.SysFont("Rosewood Std Regular", 70)
        self.myfont2 = pygame.font.SysFont("Rosewood Std Regular", 30)
        self.backgrounds = Images.background()
        self.backgrounds.background1 = self.backgrounds.set_size(self.backgrounds.background1,
                                                                 (5000, self.screen.get_height()))
        self.events = events()
    def lopp_game_over (self,score, name, records):
        records.add_record(score)
        while True:
            ev = self.events.event()
            self.screen.blit(self.backgrounds.background1,(0,0))
            self.print_game_over(score,name)
            records.print_top10(20,10,30,False)
            pygame.display.update()
            if ev == "esc":
                return True, records.name
            elif ev == "enter":
                return False, records.name

    def print_game_over(self,score, name):
        g_O = "GAME OVER"
        option1 = "Prees ENTER to restart"
        option2 = "or ESC back to menu"
        label_G_O =  self.myfont1.render(str(g_O), 1, (0, 0, 0))
        label_1 = self.myfont2.render(str(option1), 1, (255, 255, 255))
        label_2 = self.myfont2.render(str(option2), 1, (255, 255, 255))
        lanel_name = self.myfont1.render(name, 1, (255, 255, 255))

        self.screen.blit(label_G_O,(200,100))
        self.screen.blit(lanel_name, (250, 180))
        score.print_score(self.screen,(300,220))
        self.screen.blit(label_1, (230, 300))
        self.screen.blit(label_2, (230, 330))

class menu (object):
    def __init__(self,screen):
        self.screen = screen
        self.backgrounds = Images.background()
        self.backgrounds.background1 = self.backgrounds.set_size(self.backgrounds.background1,
                                                                 (5000, self.screen.get_height()))
        self.myfont1 = pygame.font.SysFont("Rosewood Std Regular", 70)
        self.events = events()
        self.pointer = Images.pointer()
        self.pos = (210,120)
    def loop_menu(self,records):
        while True:
            ev = self.events.event()
            self.screen.blit(self.backgrounds.background1,(0,0))
            self.screen.blit(self.pointer.po_img,self.pos)
            self.print_menu()
            opt = self.select(ev)
            if opt == 1:
                break
            elif opt == 2:
                records.print_top10(230,100,30,True)
            elif opt == 3:
                pygame.quit()
                exit()
            pygame.display.update()

    def print_menu(self):
        start = "START"
        records = "RECORDS"
        exit = "EXIT"
        label_start = self.myfont1.render(start, 1, (255, 255, 255))
        label_records = self.myfont1.render(records, 1, (255, 255, 255))
        label_exit = self.myfont1.render(exit, 1, (255, 255, 255))
        self.screen.blit(label_start, (230, 100))
        self.screen.blit(label_records, (230, 200))
        self.screen.blit(label_exit, (230, 300))

    def select(self,ev):
        x,y = self.pos
        if ev == "down":
            pygame.mixer.music.load("./music/select01.ogg")
            pygame.mixer.music.play()
            if y == 120:
                y = 220
            elif y == 220:
                y = 320
            else:
                y = 120
        elif ev == "up":
            pygame.mixer.music.load("./music/deselect01.ogg")
            pygame.mixer.music.play()
            if y == 120:
                y = 320
            elif y == 220:
                y = 120
            else:
                y = 220

        elif ev == "enter":
            pygame.mixer.music.load("./music/twink.ogg")
            pygame.mixer.music.play()
            if y == 120:
                return 1
            elif y == 220:
                return 2
            else:
                return 3
        self.pos = x,y
        return 0


class records(object):
    def __init__(self,screen):
        self.screen = screen
        self.name = ""
        self.backgrounds = Images.background()
        self.backgrounds.background1 = self.backgrounds.set_size(self.backgrounds.background1,
                                                                 (5000, self.screen.get_height()))
        self.eventes = events()
        self.myfont1 = pygame.font.SysFont("Rosewood Std Regular", 30)
        self.list_records = []
        try:
            records = open("records.txt","rb")
            self.list_records = pickle.load(records)
            records.close()
        except:
            pass
    def start(self):
        your_name= "your name:"
        while True:
            ev = self.eventes.event()
            self.screen.blit(self.backgrounds.background1, (0, 0))
            label_your_name = self.myfont1.render(your_name, 1, (255, 255, 255))
            label_name = self.myfont1.render(self.name, 1, (255, 255, 255))
            self.screen.blit(label_your_name,(230,100))
            self.screen.blit(label_name, (230, 200))
            if len (ev) == 1:
                pygame.mixer.music.load("./music/select01.ogg")
                pygame.mixer.music.play()
                self.name += ev
            elif ev == "b_space":
                pygame.mixer.music.load("./music/deselect01.ogg")
                pygame.mixer.music.play()
                if len(self.name) > 0:
                    self.name = self.name[0:len(self.name)-1]
            elif ev == "enter":
                pygame.mixer.music.load("./music/twink.ogg")
                pygame.mixer.music.play()
                break

            pygame.display.update()

    def print_top10(self, pos_x,pos_y,acres_y, back):
        wh = True
        while wh:
            wh = back
            y = pos_y
            if back:
                ev = self.eventes.event()
                self.screen.blit(self.backgrounds.background1, (0, 0))
                if ev == "enter" or ev =="esc":
                    break
            for record in self.list_records:
                label_name = self.myfont1.render(record["name"] +": "+str(record["score"]), 1, (255, 255, 255))
                self.screen.blit(label_name,(pos_x,y))
                y += acres_y

            pygame.display.update()

    def add_record(self, score):
        dict = {"name": self.name, "score": score.score}
        help_dict = dict
        i = 0
        help_name = False
        name = ""
        for record in self.list_records:
            if record["name"] == self.name:
                help_name = True
                name= self.name
                break

        if len(self.list_records) > 0:
            for record in self.list_records:
                if record["score"] < dict["score"]:
                    help_dict = record
                    self.list_records[i] = dict
                    dict = help_dict
                    if help_name and dict["name"] == name:
                        break
                i +=1
            if len(self.list_records) < 10 and not help_name:
                self.list_records.append(dict)

        else:
            self.list_records.append(dict)

        records = open("records.txt", "wb")
        pickle.dump(self.list_records, records)
        records.close()


