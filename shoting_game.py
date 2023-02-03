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

    def show_background(self):
        # show the background
        screen.blit(self.background, (0,0))
    
    def show_buttons(self):
        # show the buttons
        screen.blit(self.play, self.play_rect)
        screen.blit(self.quit, self.quit_rect)
        screen.blit(self.option, self.option_rect)

    # setting up the option button
    def option_button(self):
        pos = pygame.mouse.get_pos()

        if self.option_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]:
                self.root = Tk()
                self.center_window(self.root, 400, 400)

                # the tkinter window will always stays on top of other windows
                self.root.attributes('-topmost', True)


                # create a scale to control the music value
                scale = Scale(self.root, from_=0, to=100, orient=HORIZONTAL, command=self.set_volume, width=20)
                scale.set(10) # set the initial value to 50
                
                # create a text near the scale
                scale_text = Label(self.root, text='Volume:', font=('Times', 25))

                # create a setting text
                setting_text = Label(self.root, text='Setting', font=('System', 35))

                # show the settings text
                setting_text.grid(row=0, column=0, columnspan=10, pady=10, padx=135, sticky='nsew')

                # show the scale and the scale text
                scale.grid(row=2, column=1, sticky='w')
                scale_text.grid(row=2, column=0, pady=5)


                self.root.mainloop()

    def center_window(self, root, window_width, window_height):
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_coord = (screen_width/2) - (window_width/2)
        y_coord = (screen_height/2) - (window_height/2)
        root.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coord, y_coord))
    
    def set_volume(self, val):
        volume = float(val) / 100
        mixer.music.set_volume(volume)


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


    pygame.display.update()
    clock.tick(120)