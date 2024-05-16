from pygame import *
from random import randint
import time as tm
import os, datetime
#vars~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def new_vector():
    startx = randint(1,2)
    starty = randint(1,2)
    if startx == 1:
        speed_x = 2.5
    else: 
        speed_x = -2.5
    if starty == 1:
        speed_y = 2.5
    else: 
        speed_y = -2.5
plsyer1_csore = 0; up = True; choose_1 = False; startx = randint(1,2)
plsyer2_csore = 0; down = False; choose_2 = False; starty = randint(1,2)
#classes~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class GameSprite(sprite.Sprite):
    def __init__(self,sizex, sizey, pImage,sped,xcor,ycor):
        super().__init__()
        self.xSize = sizex
        self.ySize = sizey
        self.image = transform.scale(image.load(pImage),(self.xSize,self.ySize))
        self.speed = sped
        self.rect = self.image.get_rect()
        self.rect.x = xcor
        self.rect.y = ycor
    def show(self):
        wind.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def walking(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_e] and self.rect.y < 450:
            self.rect.y += self.speed
        if keys_pressed[K_d] and self.rect.y > 0:
            self.rect.y -= self.speed
class Playerr(GameSprite):
    def walking(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_o] and self.rect.y < 450:
            self.rect.y += self.speed
        if keys_pressed[K_k] and self.rect.y > 0:
            self.rect.y -= self.speed
class Ball(GameSprite):
    global startx, starty, up, down
    if startx == 1:
        speed_x = 4
    else: 
        speed_x = -4
    if starty == 1:
        speed_y = 4
    else: 
        speed_y = -4
    if startx == 1 and starty == 1:
        up = False; down = True
    def move(self):
        self.rect.x += self.speed_x
        self.rect.y -= self.speed_y
        if self.rect.y >= 0:
            self.speed_y = -self.speed_y
        if self.rect.y <= 550:
            self.speed_y = -self.speed_y
class CPU(GameSprite):
    def walking(self):
            global up,down
            if up:
                if self.rect.y > 0:
                    self.rect.y -= self.speed
                else:
                    up = False; down = True
            if down:
                if self.rect.y < 450:
                    self.rect.y += self.speed
                else:
                    down = False; up = True
#window~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
win_h = 800; win_w = 600
wind = display.set_mode((win_h,win_w))
display.set_caption("Ping-Pong")
bg = transform.scale(image.load("bg.png"), (win_h, win_w))
clock = time.Clock()
#font~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
font.init()
defaultFont = font.SysFont("Arial", 64, 1)
chooseFont = font.SysFont("Times", 32, 1)
#sounds~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
mixer.init()
mixer.music.load(open("music.ogg"))
mixer.music.play()
#sprites~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
player1 = Player(40,150, "new_platform.png",10,5,250)
player2 = Playerr(40,150, "new_platform.png",10,755,250)
cpu = CPU(40,150, "new_platform.png",12,755,250)
choose_1_text = chooseFont.render("→ Player VS Player ←",1, (255,255,255))
choose_2_text = chooseFont.render("→ Player VS CPU ←",1,(255,255,255))
players = sprite.Group(); players.add(player1); players.add(player2)
sphere =  Ball(50,50,"ball.png",2,400,300)
#funcs~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def save_stat():
    date = datetime.datetime.now()
    global_score = str(plsyer1_csore)+":"+str(plsyer2_csore)
    if choose_2: text = "Time: "+str(date)+"\n"+"Mode: → Player VS CPU ←"+"\n"+"Score: "+str(global_score)+"\n \n"
    else: text =  text = "Time: "+str(date)+"\n"+"Mode: → Player VS Player ←"+"\n"+"Score: "+str(global_score)+"\n \n"
    with open("Ping-Pong_Statistic.txt", "a", encoding="utf-8") as file:
        file.write(text)
        print("Statistic was wrote.")
def close_stat():
    with open("Ping-Pong_Statistic.txt", "a", encoding="utf-8") as file:
        file.write(""*10+"Game was closed \n")
        file.write("~"*60+"\n")    
def open_stat():
    with open("Ping-Pong_Statistic.txt", "a", encoding="utf-8") as file:
        file.write("~"*60+"\n")
        file.write(""*10+"Game was opened \n \n")
#cycle~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
game = True; finish = False; choosen = False; setable = True; clicked = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False; close_stat()
        if e.type == MOUSEBUTTONDOWN:
            getted_position = mouse.get_pos()
            if getted_position[1] >= 300 and setable:
                choose_1 = True 
                open_stat();cpu.kill()
                print("PvP mode was choosed")
                setable = False 
            if getted_position[1] < 300 and setable: 
                choose_2 = True
                open_stat(); player2.kill()
                print("PvC mode was choosed")
                setable = False
        if e.type == KEYDOWN:
            keys_pressed = key.get_pressed()    
    if choose_1 == False or choose_2 == False and choosen == False:
            wind.blit(bg,(0,0))
            wind.blit(choose_2_text, (250,125))
            wind.blit(choose_1_text, (250,425))
    if choose_1 or choose_2:
        choosen = True
    if finish != True and choosen: 
        wind.blit(bg,(0,0))
        lose1 = defaultFont.render("PLAYER 1 WINS!",1,(randint(0,255),randint(0,255),randint(0,255)))
        lose2 = defaultFont.render("PLAYER 2  WINS!",1,(randint(0,255),randint(0,255),randint(0,255)))
        players_score = defaultFont.render(f"{plsyer1_csore}:{plsyer2_csore}", 1,(randint(0,255),randint(0,255),randint(0,255)))
        wind.blit(players_score,(360,25))   
        player1.show(); player1.walking()
        if choose_1:
            player2.show(); player2.walking()
        if choose_2:
            cpu.show(); cpu.walking()
        sphere.show(); sphere.move()
        if player1.rect.colliderect(sphere):
            sphere.speed_x *= -1
        if choose_1:
            if player2.rect.colliderect(sphere):
                sphere.speed_x *= -1
        if choose_2:
            if cpu.rect.colliderect(sphere):
                sphere.speed_x *= -1
        if sphere.rect.x <= 0: 
            plsyer2_csore += 1; sphere.kill(); time.delay(1200)
            sphere =  Ball(50,50,"ball.png",2,400,300)
        if sphere.rect.x >= 800:
            plsyer1_csore += 1; sphere.kill(); time.delay(1200)
            sphere =  Ball(50,50,"ball.png",2,400,300)
        if plsyer1_csore == 7:
            wind.blit(lose1,(210,260)); finish = True
        if plsyer2_csore == 7:
            wind.blit(lose2,(210,260)); finish = True
    else: 
        if choosen:
            counter = 0
            while counter != 3:
                if plsyer1_csore == 7:
                    wind.blit(lose1,(210,260))
                if plsyer2_csore == 7:
                    wind.blit(lose2,(210,260))
                tm.sleep(1.2); counter += 1
            save_stat(); finish = False; counter = 0
            plsyer1_csore = 0; plsyer2_csore = 0
            sphere.kill();sphere =  Ball(50,50,"ball.png",2,400,300)
            
    display.update(); clock.tick(60)