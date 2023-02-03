import random
import time
import pygame
from tkinter import messagebox
import pyautogui
from pyautogui import *
import csv
from pygame import mixer
from tkinter import *

# create the start screen
class start_screen:
    def __init__(self):
        # background sound
        mixer.init()
        mixer.music.load('songs/start_song.mp3')
        mixer.music.play(-1)
        mixer.music.set_volume(0.1)


        # background
        self.background = pygame.image.load('them/background.png').convert_alpha()

        # all the buttons
        # play
        self.play = pygame.image.load('buttons/play.png').convert_alpha()
        self.play_rect = self.play.get_rect(center=(800, 400))

        # quit
        self.quit = pygame.image.load('buttons/quit.png').convert_alpha()
        self.quit_rect = self.quit.get_rect(center=(800, 500))

        # option
        self.option = pygame.image.load('buttons/option.png').convert_alpha()
        self.option_rect = self.option.get_rect(center=(800, 600))

        # volume
        self.volume = 10

        # check if you can play
        self.play_check = False

        # get a check of the number of the level and the x,y position
        self.num_level = 0

        self.y_levels = 115
        self.x_levels = 200

        # create a list to store all the levels rect
        self.levels_rect_list = []
        self.levels_list = []

    def show_background(self):
        # show the background
        screen.blit(self.background, (0,0))
    
    def show_buttons(self):
        # show the buttons
        screen.blit(self.play, self.play_rect)
        screen.blit(self.quit, self.quit_rect)
        screen.blit(self.option, self.option_rect)

    def set_volume(self, val):
        self.volume = float(val) / 100
        mixer.music.set_volume(self.volume)
        self.volume = self.volume * 100
        
    # setting up the option button
    def option_button(self):
        pos = pygame.mouse.get_pos()


        if self.option_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]:
                self.root = Tk()
                self.root.title('Settings')
                self.center_window(self.root, 400, 400)

                # the tkinter window will always stays on top of other windows
                self.root.attributes('-topmost', True)


                # create a scale to control the music value
                scale = Scale(self.root, from_=0, to=100, orient=HORIZONTAL, command=self.set_volume, width=20)
                scale.set(self.volume) # set the initial value to 50
                self.volume = scale.get()
            
                
                # create a text near the scale
                scale_text = Label(self.root, text='Volume:', font=('Times', 25))

                # create a setting text
                setting_text = Label(self.root, text='Setting', font=('System', 35))

                # show the settings text
                setting_text.grid(row=0, column=0, columnspan=10, pady=10, padx=135, sticky='nsew')

                # show the scale and the scale text
                scale.grid(row=2, column=1, sticky='w')
                scale_text.grid(row=2, column=0, pady=5)

                # check if he closed the screen
                self.root.protocol("WM_DELETE_WINDOW", self.closed_tkinter)

                self.root.mainloop()

    def closed_tkinter(self):
        self.root.destroy()
        pyautogui.click()

    def center_window(self, root, window_width, window_height):
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_coord = (screen_width/2) - (window_width/2)
        y_coord = (screen_height/2) - (window_height/2)
        root.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coord, y_coord))
    
    def quit_(self):
        pos = pygame.mouse.get_pos()

        if self.quit_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]:
                exit()

    def play_(self):
        pos = pygame.mouse.get_pos()

        if self.play_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]:
                self.play_check = True

        # check if he can play
        if self.play_check == True:
            self.pick_level()
    
    def pick_level(self):
        self.handle_back_button()
        self.show_levels()

        

    def show_levels(self):
        if self.num_level <= 19:
            levels = pygame.image.load(f'levels/level {self.num_level + 1}.png').convert_alpha()
            levels_rect = levels.get_rect(center=(self.x_levels, self.y_levels))

            self.num_level += 1
            self.y_levels += 115
            
            
            # store the values in a lists
            self.levels_list.append(levels)
            self.levels_rect_list.append(levels_rect)

            # increase the x on the rect of the levels and rest the y
            if self.num_level % 5 == 0:
                self.x_levels += 400
                self.y_levels = 115
                


        for level, rect in zip(self.levels_list, self.levels_rect_list):
                screen.blit(level, rect)


    def handle_back_button(self):     
        # un show all the thing on the screen
        self.quit_rect = self.quit.get_rect(center=(-100, -1000))
        self.play_rect = self.play.get_rect(center=(-100, -1000))
        self.option_rect = self.option.get_rect(center=(-100, -1000))

        # create a back button
        back_button = pygame.image.load('buttons/Back.png').convert_alpha()
        back_button_rect = back_button.get_rect(center=(160, 750))
        
        # show him
        screen.blit(back_button, back_button_rect)

        # call the function of the back button
        self.back_button_function(back_button_rect)
        
    def back_button_function(self, back_button_rect):
        pos = pygame.mouse.get_pos()

        if back_button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]:
                self.play_check = False
                self.__init__()

# create the screen
pygame.init()
screen = pygame.display.set_mode((1600,800))
title = pygame.display.set_caption("Asteroid")
clock = pygame.time.Clock()

# create the start screen instance
s = start_screen()

# start the loop of the game
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    
    # start screen
    s.show_background()
    s.show_buttons()
    s.option_button()
    s.quit_()
    s.play_()

    pygame.display.update()
    clock.tick(120)