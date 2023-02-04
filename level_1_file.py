import random
import time
import pygame
from tkinter import messagebox
import pyautogui
from pyautogui import *
import csv
from pygame import mixer
from tkinter import *


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
        self.bullets_speed = 15
        self.bullets_velocity_x = 0

        # create a list to store all the bullets
        self.bullets_list = []

        # check if you shot
        self.check_shot = False


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

        # enami spawn limit
        self.enami_speed = 20


    def show_background(self):        
        # get the size of the screen
        info = pygame.display.Info()
        screen_width = info.current_w
        screen_height = info.current_h

        # background
        background = pygame.image.load('texture/background/background2.png').convert_alpha()
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
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_SPACE]:
            self.bullet_rect = self.bullet.get_rect(center=(self.player_rect.x+90, self.player_rect.y+60))

            # append the self.bullet_rect in the list to store it
            self.bullets_list.append(self.bullet_rect)

            # make it true
            self.check_shot = True

        if self.check_shot == True:
            for rect in self.bullets_list:
                self.bullets_velocity_x = self.bullets_speed

                rect.x += self.bullets_velocity_x
                screen.blit(self.bullet, rect)

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
            velocity = [ (player_center[0] - rect.centerx) / 10, (player_center[1] - rect.centery) / 10 ]
            rect.x += velocity[0]
            rect.y += velocity[1]
            for other_rect in self.enamis_list:
                if rect != other_rect and rect.colliderect(other_rect):
                    rect.x -= velocity[0]
                    rect.y -= velocity[1]
            screen.blit(self.enami, rect)

                
        # show the player
        screen.blit(self.player, self.player_rect)
            


# create the screen
pygame.init()
screen = pygame.display.set_mode((1600,800))
title = pygame.display.set_caption("Asteroid")
clock = pygame.time.Clock()

# create the object of start level one
level_one = start_level_one()

# start the loop
while True:
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



    level_one.show_background()
    level_one.player_movement()
    level_one.shot_bullet()
    level_one.enami_settings()

    pygame.display.update()
    clock.tick(120)