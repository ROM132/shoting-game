import random
import time
import pygame
from tkinter import messagebox
import pyautogui
from pyautogui import *
import csv
from pygame import mixer
from tkinter import *
import math



class start_level_one:
    def __init__(self):
        # create a the player and the player rect
        self.player = pygame.image.load('texture/player.png').convert_alpha()
        self.player_rect = self.player.get_rect(center=(800,400))

        # defined a velocity to the player
        self.velocity_x = 0
        self.velocity_y = 0

        # speed
        self.player_speed = 35

        # thing to check
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # bullet 
        self.bullet = pygame.image.load('texture/bullet.png').convert_alpha()
        self.bullet_rect = self.bullet.get_rect(center=(self.player_rect.x+90, self.player_rect.y+50))

        # defined the velocity and the speed of the bullets
        self.bullets_speed = 25
        self.bullets_velocity_x = 0

        # create a list to store all the bullets
        self.bullets_list = []

        # check if you shot
        self.check_shot = False

        # delay time shot
        self.delay_time_shot = 100

        # enami
        self.enami = pygame.Surface((30, 30)).convert_alpha()
        self.enami.fill((255, 0, 0))

        # delay before respawn the enami
        self.delay_respawn_enami = 2000  # 2000 mil == 2 seconds

        # check if he can spawn
        self.can_spawn_enami = False

        # defined a list that store all the enamis
        self.enamis_list = []

        # i dont need this but i have to put this here dont mind dont mind
        self.last_enami_spawn = pygame.time.get_ticks()
        self.last_shot_time = pygame.time.get_ticks()
        self.time = 0
        self.bullets_collect_rect = None
        self.current_time = pygame.time.get_ticks()


        # enami spawn limit
        self.enami_speed = 10

        # settings
        self.settings = pygame.image.load('texture/settings.png').convert_alpha()
        self.settings_rect = self.settings.get_rect(topleft=(0,0))

        # create a list to check how much bullet are shots until now and a variable that control if you can shot
        self.bullet_full_list = []
        self.bullet_can_shot = True
        self.bullet_num = 15

        # create the texture of the collectable bullets
        self.collectable_bullets = pygame.image.load('texture/collected_bullets.png').convert_alpha()

        # check if he collect the bullet
        self.collect_bullet_check = False

        # the spawn point of the bullets collector
        self.spawn_bullets_x = random.randint(0, 1515)
        self.spawn_bullets_y = random.randint(0, 720)

        # check if he closed the settings
        self.closed_settings = False

        self.root = Tk()
        self.root.title('Settings')
        self.root.destroy()

        # add sound of shot
        self.shot_sound = pygame.mixer.Sound('songs/Laser Shot.wav')

        # appear bullets sound
        self.appear_bullets_sound = pygame.mixer.Sound('songs/appear.ogg')



    def show_background(self):       
        # get the size of the screen
        info = pygame.display.Info()
        screen_width = info.current_w
        screen_height = info.current_h

        # background
        background = pygame.image.load('texture/background/background2.png').convert()
        image = pygame.transform.scale(background, (screen_width, screen_height))
        
        # show the background on the screen
        screen.blit(image, (0, 0))

    def player_movement(self):
        self.angle = 0

        self.velocity_x = 0
        self.velocity_y = 0

        if self.left_pressed and not self.right_pressed:
            self.velocity_x = -self.player_speed

        if self.right_pressed and not self.left_pressed:
            self.velocity_x = self.player_speed


        if self.up_pressed and not self.down_pressed:
            self.velocity_y = -self.player_speed

        if self.down_pressed and not self.up_pressed:
            self.velocity_y = self.player_speed

        # called the board function to check
        self.board()

        self.player_rect.x += self.velocity_x
        self.player_rect.y += self.velocity_y

    # create a board for the player
    def board(self):
        # check the x
        if self.player_rect.x >= 1515:
            self.player_rect.x = 1514
        if self.player_rect.x <= -15:
            self.player_rect.x = -14

        # check the y
        if self.player_rect.y >= 720:
            self.player_rect.y = 722
        if self.player_rect.y <= -15:
            self.player_rect.y = -14
        
    def shot_bullet(self):
        if self.bullet_can_shot == True:
            keys = pygame.key.get_pressed()
            
            if keys[pygame.K_SPACE] and self.check_shot:  
                self.shot_sound.play()
                self.last_shot_time = pygame.time.get_ticks()

                self.bullet_rect = self.bullet.get_rect(center=(self.player_rect.x+90, self.player_rect.y+60))

                # append the self.bullet_rect in the list to store it
                self.bullets_list.append(self.bullet_rect)
                self.bullet_full_list.append(self.bullet_rect)

                # make it true
                self.check_shot = False

            if not self.check_shot:
                time_since_last_shot  = pygame.time.get_ticks() - self.last_shot_time

                if time_since_last_shot >= self.delay_time_shot:  # 500 milliseconds = 0.5 seconds
                    self.check_shot = True

            
        for rect in self.bullets_list:
            self.bullets_velocity_x = self.bullets_speed

            rect.x += self.bullets_velocity_x
            screen.blit(self.bullet, rect)

    # create a function that control how much shot you have
    def bullet_num_control(self):
        if len(self.bullet_full_list) == self.bullet_num:
            self.bullet_can_shot = False
        else:
            self.bullet_can_shot = True

    # defined a function that let you collect bullets
    def collect_bullets(self):
        # create his rect
        self.bullets_collect_rect = self.collectable_bullets.get_rect(center=(self.spawn_bullets_x, self.spawn_bullets_y))

        # make it move up and down
        self.time += 0.5
        self.bullets_collect_rect.y = self.spawn_bullets_y + 20 * math.sin(self.time)

        # show it on the screen 
        screen.blit(self.collectable_bullets, self.bullets_collect_rect)

    def show_current_bullets(self): 
        current_bullets = self.bullet_num- len(self.bullet_full_list)

        # text that going to show how much bullets you have
        current_bullets_font = pygame.font.Font(None, 50)
        text_bullets_current = current_bullets_font.render(f"bullets: {current_bullets}", False, "black").convert_alpha()
        text_bullets_current_rect = text_bullets_current.get_rect(topleft= (0,60))

        # show him on the screen
        screen.blit(text_bullets_current, text_bullets_current_rect)

    # check if he collect a bullets and add it to is bullets number
    def collision_collect_bullets_and_player(self):
        random_amount_bullets = random.randint(1, 10)
        # check for collision
        if self.player_rect.colliderect(self.bullets_collect_rect):
            # add an appear sound
            self.appear_bullets_sound.play()

            # get the time
            self.current_time = pygame.time.get_ticks()

            # add a random amount of bullets
            self.bullet_num += random_amount_bullets
            self.spawn_bullets_x = random.randint(0, 1515)
            self.spawn_bullets_u = random.randint(0, 720)

            # text that going to show how much bullets you get
            self.text_bullets_font = pygame.font.Font(None, 100)
            self.text_bullets = self.text_bullets_font.render(f"+{random_amount_bullets}", False, "black").convert_alpha()
            self.text_bullets_rect = self.text_bullets.get_rect(center= (800,30))
        
        self.update()
        # update the text display time
    def update(self):
                # check if the current time is less than the start time + 3000 milliseconds (3 seconds)
        try:
            if pygame.time.get_ticks() < self.current_time + 2000:
                screen.blit(self.text_bullets, self.text_bullets_rect)
        except:
            pass

    def enami_settings(self):
        if self.can_spawn_enami:
            # take the time
            self.last_enami_spawn = pygame.time.get_ticks()

            # x,y to spawn
            spawn_x_enami = random.randint(0, 1515)
            spawn_y_enami = random.randint(0, 720)

            # create the enami rect
            enami_rect = self.enami.get_rect(center=(spawn_x_enami,spawn_y_enami))

            # append all the enami to the list
            self.enamis_list.append(enami_rect)
            self.can_spawn_enami = False
            
        if not self.can_spawn_enami:
            time_since_last_spawn  = pygame.time.get_ticks() - self.last_enami_spawn
            if time_since_last_spawn >= self.delay_respawn_enami:  # 2000 milliseconds = 2 seconds
                self.can_spawn_enami = True


        player_center = self.player_rect.center
        for rect in self.enamis_list:
            velocity = [ (player_center[0] - rect.centerx) / self.enami_speed, (player_center[1] - rect.centery) / self.enami_speed ]
            rect.x += velocity[0]
            rect.y += velocity[1]
            for other_rect in self.enamis_list:
                if rect != other_rect and rect.colliderect(other_rect):
                    rect.x -= velocity[0]
                    rect.y -= velocity[1]
            screen.blit(self.enami, rect)

                
        # show the player
        screen.blit(self.player, self.player_rect)

    def collision_enami_bullet(self):
        for bullet_rect in self.bullets_list:
            for enami_rect in self.enamis_list:

                # check for collision
                if bullet_rect.colliderect(enami_rect):
                    # remove the bullet and the enami
                    try:
                        self.enamis_list.remove(enami_rect)
                        self.bullets_list.remove(bullet_rect)
                    except:
                        pass
    
    def settings_fun(self):
        screen.blit(self.settings, self.settings_rect)
        pos = pygame.mouse.get_pos()

        if self.settings_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]:
                try:
                    self.root = Tk()
                    print('work')
                except:
                    pass
                self.center_window(self.root, 400, 400)

                # create the settings





                # the tkinter window will always stays on top of other windows
                self.root.attributes('-topmost', True)


                # check if he closed the screen
                self.root.protocol("WM_DELETE_WINDOW", self.closed_tkinter)


                self.root.mainloop()
    
    def closed_tkinter(self):
        self.root.destroy()
    
    def center_window(self, root, window_width, window_height):
        screen_width = 1920
        screen_height = 1080
        x_coord = (screen_width/2) - (window_width/2)
        y_coord = (screen_height/2) - (window_height/2)
        root.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coord, y_coord))
        

# create the screen
pygame.init()
running = True

screen = pygame.display.set_mode((1600,800))
title = pygame.display.set_caption("Shooting game")
clock = pygame.time.Clock()

# create the object of start level one
level_one = start_level_one()

# start the loop
while running == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        # player movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                level_one.left_pressed = True


            if event.key == pygame.K_d:
                level_one.right_pressed = True


            if event.key == pygame.K_w:
                level_one.up_pressed = True


            if event.key == pygame.K_s:
                level_one.down_pressed = True



        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                level_one.left_pressed = False

            if event.key == pygame.K_d:
                level_one.right_pressed = False

            if event.key == pygame.K_w:
                level_one.up_pressed = False

            if event.key == pygame.K_s:
                level_one.down_pressed = False

    screen.fill((0, 0, 0)) 

    level_one.show_background()
    level_one.player_movement()
    level_one.shot_bullet()
    level_one.bullet_num_control()
    level_one.collect_bullets()
    level_one.show_current_bullets()
    level_one.collision_collect_bullets_and_player()
    level_one.enami_settings()
    level_one.collision_enami_bullet()
    level_one.settings_fun()

    pygame.display.update()
    clock.tick(165)