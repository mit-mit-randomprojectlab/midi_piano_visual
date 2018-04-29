#!/usr/bin/python

"""
main.py - Main entry point for game
"""

import pygame
from pygame.locals import *
import pygame.midi

from gamedirector import *
from game import *

# Start
def main(mainpath,fullscreen=False):

    # Initialise pygame
    pygame.init()
    if fullscreen:
    	pygame.mouse.set_visible(False)
    
    # Initialise midi
    pygame.midi.init()
    
    # start up director
    framerate = 30
    screen_res = (640,480)
    window_title = "py_piano"
    dir = GameDirector(window_title, screen_res, framerate, fullscreen)
    
    # Load game scenes
    maingame = MainGame(dir, screen_res)
    dir.addscene('maingame', maingame)
    
    # start up director
    dir.change_scene('maingame', [])
    dir.loop()

