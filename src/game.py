#!/usr/bin/python

"""
game.py - main in-game scene classes
"""

import os
import pygame
from pygame.locals import *
from gamedirector import *

import random
import colorsys

FW_FLYSPEED = 1.0/30.0
FW_EXPLODESPEED = 0.5/30.0
FW_BLIPSIZE = 0.01
FW_WAVESIZE = 0.01

class Firework(object):
	def __init__(self,parent,pos_x,colour,intensity):
		self.parent = parent
		self.pos_x = pos_x
		self.pos_y = 1.0
		self.colour = colour
		self.intensity = intensity
		self.to_y = 0.8*random.random()+0.1
		
		self.state = 'flying'
		self.radius = 0
	
	def Update(self):
		
		if self.state == 'flying':
			self.pos_y -= FW_FLYSPEED
			if self.pos_y < self.to_y:
				self.state = 'explode'
		elif self.state == 'explode':
			self.radius += FW_EXPLODESPEED
			if self.radius > 0.3:
				self.state = 'finished'
	
	def Draw(self,screen):
		if self.state == 'flying':
			blip_size = max(int(self.parent.window_size[0]*FW_BLIPSIZE),1)
			pygame.draw.circle(screen, self.colour, (int(self.parent.window_size[0]*self.pos_x),int(self.parent.window_size[1]*self.pos_y)), blip_size, 0)
		elif self.state == 'explode':
			radius = max(1,int(self.parent.window_size[0]*self.radius))
			wave_size = max(int(self.parent.window_size[0]*FW_WAVESIZE),1)
			if wave_size > radius:
				wave_size = radius
			pygame.draw.circle(screen, self.colour, (int(self.parent.window_size[0]*self.pos_x),int(self.parent.window_size[1]*self.pos_y)), radius, wave_size)

class MainGame(GameScene):
    def __init__(self, director, window_size):
        super(MainGame, self).__init__(director)
        self.window_size = window_size
        
        # frame rate recording
        self.avgframerate = -1
        self.frsamples = 0
        
        # Background
        self.background = pygame.Surface(window_size)
        self.background.fill((0,0,0))
        self.background.convert()
        
        self.key_press = False
        
    def on_switchto(self, switchtoargs):
    	
    	self.fireworks = []
        self.fire_colour_ind = 0.0
    	
    	i = 0
    	good_list = []
    	print('Detecting MIDI devices available ...')
    	while True:
    		info = pygame.midi.get_device_info(i)
    		if info == None:
    			break
    		if info[2] == 0: # not an input device
    			i += 1
    			continue
    		print("device: %d"%(i),info)
    		good_list.append(i)
    		i += 1
    	if len(good_list) == 0:
    		print('No MIDI devices found, exiting ...')
    		self.director.change_scene(None, [])
    		return
    	elif len(good_list) == 1:
    		i_select = good_list[0]
    	else:
    		name = raw_input("Enter MIDI device ID for piano: ")
    		try:
    			i_select = int(name)
    		except:
    			print('invalid option')
    			self.director.change_scene(None, [])
    			return
    	
    	print('connecting to device %d ...'%(i_select))
        self.midi = pygame.midi.Input(i_select)
        
    def on_update(self):
        
        if self.director.quit_flag:
        	return
        	
        # Clean up finished fireworks
        remove_list = []
        for fw in self.fireworks:
        	if fw.state == 'finished':
        		remove_list.append(fw)
        for fw in remove_list:
        	self.fireworks.remove(fw)
        
        # Update
        for fw in self.fireworks:
        	fw.Update()
        
        # look for creating new ones (based on keyboard)
        if self.key_press:
        	colour = tuple([int(255*i) for i in colorsys.hsv_to_rgb(self.fire_colour_ind,1.0,1.0)])
        	self.fireworks.append(Firework(self,0.8*random.random()+0.1,colour,1))
        	self.fire_colour_ind += 0.08
        	if self.fire_colour_ind > 1.0:
        		self.fire_colour_ind = 0.0
        
        # look for creating new ones (based on MIDI keyboard)
        b_msg = self.midi.poll()
        if b_msg == True:
            while True:
                data = self.midi.read(1)
                if len(data) == 0:
                    break
                (type,note,vel,stuff) = data[0][0]
                if vel > 0:
                	x_pos = (0.8*(note-36)/(96.0-36.0) + 0.1)
                	colour = tuple([int(255*i) for i in colorsys.hsv_to_rgb(self.fire_colour_ind,1.0,1.0)])
                	self.fireworks.append(Firework(self,x_pos,colour,1))
                	self.fire_colour_ind += 0.08
                	if self.fire_colour_ind > 1.0:
                		self.fire_colour_ind = 0.0
        
    def on_event(self, events):
    	
    	if self.director.quit_flag:
        	return
    	
    	self.key_press = False
        for event in events:
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                self.director.change_scene(None, [])
            if event.type == KEYDOWN and event.key == K_a:
            	self.key_press = True
                
    def on_draw(self, screen):
        screen.blit(self.background, (0, 0))
        for fw in self.fireworks:
        	fw.Draw(screen)
        
