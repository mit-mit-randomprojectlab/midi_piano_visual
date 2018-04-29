#!/usr/bin/python

"""
gamedirector.py - classes for running the game using a director/scene structure
"""

import pygame
from pygame.locals import *

class GameDirector(object):
    def __init__(self, title, window_size, fps, fullscreen=False):
        if fullscreen:
            self.screen = pygame.display.set_mode((window_size[0], window_size[1]), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((window_size[0], window_size[1]))
        pygame.display.set_caption(title)
        self.fps = fps
        self.scene = None
        self.scenelist = {}
        self.quit_flag = False
        self.clock = pygame.time.Clock()
        self.frame = 0
        self.timesincestart = 0
    
    def loop(self):
        while not self.quit_flag:
            self.time = self.clock.tick(self.fps)
            self.framerate = 1000.0/self.time
            self.frame = self.frame + 1
            self.timesincestart = self.timesincestart + self.time
            
            # Exit events
            filtered_events = []
            for event in pygame.event.get():
                quitevent = False
                if event.type == pygame.QUIT:
                    self.quit()
                    quitevent = True
                if not quitevent:
                    filtered_events.append(event)
            
            # Detect events
            self.scene.on_event(filtered_events)
            
            # Update scene
            self.scene.on_update()
            
            # Draw the screen
            self.scene.on_draw(self.screen)
            pygame.display.flip()
    
    def addscene(self, scenename, sceneobj):
        self.scenelist[scenename] = sceneobj
    
    def change_scene(self, scenename, switchtoargs):
        if scenename is None:
            self.quit()
        else:
            self.scene = self.scenelist[scenename]
            self.scene.on_switchto(switchtoargs)
        
    def quit(self):
        self.quit_flag = True

class GameScene(object):
    def __init__(self, director):
        self.director = director
    
    def on_switchto(self, switchtoargs):
        raise NotImplementedError("on_switchto abstract method must be defined in subclass.")
    
    def on_update(self):
        raise NotImplementedError("on_update abstract method must be defined in subclass.")
    
    def on_event(self, event):
        raise NotImplementedError("on_event abstract method must be defined in subclass.")
    
    def on_draw(self, screen):
        raise NotImplementedError("on_draw abstract method must be defined in subclass.")

