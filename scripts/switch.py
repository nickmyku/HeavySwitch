#!/usr/bin/env python

#Written by Nicholas Mykulowycz
#Created on May 25, 2014
#script for reading button inputs and sending commands to lights

import os
import sys
import pygame
from pygame.locals import *
from time import sleep
from time import time
from phue import Bridge
import RPi.GPIO as GPIO
from subprocess import call
import pickle   #for saving/reading variables to/from file

#load shared global variables
execfile('/home/pi/HeavySwitch/scripts/shared_globals.py')

#initialize state data array
state_data = ['0','script_terminated','bridge_disconnected','loop_terminated']

#write data to state file using pickle module
def writeStateFile(array):
	fileObj = open(STATE_PATH, 'wb')
	pickle.dump(array,fileObj)	
	#then imediately close the file
	fileObj.close()

#switch status booleans
on_state = False
color_state = False
dim_state = False

#configure pins
GPIO.setwarnings(False)		#silence pin in use warning
GPIO.setmode(GPIO.BCM)
GPIO.setup(ON_PIN, GPIO.IN)     #full om input pin
GPIO.setup(COLOR_PIN, GPIO.IN)     #color on input pin
GPIO.setup(DIM_PIN, GPIO.IN)     #dim on input pin


#set script_started line in state file - indicates script ran
state_data[0] = str(time())
state_data[1] = 'script_started'
#write to file
writeStateFile(state_data)

b = Bridge('192.168.1.202')
lights = b.get_light_objects('id')

#set bridge_connected line in state file - indicates bridge connection was set up
state_data[0] = str(time())
state_data[2] = 'bridge_connected'
#write to file
writeStateFile(state_data)

#intialize pygame
#pygame.init()
#screen = pygame.display.set_mode((640,480))	#need to set display to catch key presses
#pygame.display.set_caption('HeavySwitch')
#pygame.mouse.set_visible(0)

def setLight(light_num, on_val, hue_val, sat_val, bright_val):
	lights[light_num].on = on_val	#light must be on to change paramters
	if on_val == True:
		sleep(.1)
		lights[light_num].brightness = bright_val
		sleep(.1)
		lights[light_num].hue = hue_val
		sleep(.1)
		lights[light_num].saturation = sat_val
		sleep(.1)
	return;


def allOff():
    #define varibles as global to prevent useless local varibles from being created
    global on_state
    global color_state
    global dim_state
    lights[1].on = False
    lights[2].on = False
    lights[3].on = False
    on_state = False
    color_state = False
    dim_state = False
    setStateLabel('The lights are OFF')
    return;

def setAll(on_val, hue_val, sat_val, bright_val):
    setLight(1, on_val, hue_val, sat_val, bright_val)
    setLight(2, on_val, hue_val, sat_val, bright_val)
    setLight(3, on_val, hue_val, sat_val, bright_val)
    return;

def buttonHeld(pin):
    start_time = time()
    curr_time = time()
    
    #set the pin numbers of the other buttons based on the pin that was fed into the function
    if(pin == ON_PIN):
	alt_pin_1 = COLOR_PIN
	alt_pin_2 = DIM_PIN
    elif(pin == COLOR_PIN):
	alt_pin_1 = ON_PIN
	alt_pin_2 = DIM_PIN
    else:
	alt_pin_1 = ON_PIN
	alt_pin_2 = COLOR_PIN

    #loop continues while time elapsed is less than the hold time threashold
    #and the button is still being held AND no other buttons are pressed
    while((curr_time-start_time < HOLD_TIME) and GPIO.input(pin) == False and GPIO.input(alt_pin_1) == True and GPIO.input(alt_pin_2) == True):
        sleep(0.05);
        curr_time = time()

    #if pin is still held after loop exits button hold detected AND no other buttons are pressed
    #turn off all lights and return true
    if(GPIO.input(pin) == False and GPIO.input(alt_pin_1) == True and GPIO.input(alt_pin_2) == True):
        allOff()
        sleep(2)
        return True;
    #if button was released then it was not held return false
    else:
        return False;

print "\nswitch.py running..."
print "Press Ctrl+C or all physical buttons to terminate script\n"

def setLightsON():
	global on_state
	global color_state
	global dim_state
	setAll(True, on_Hue, on_Sat, on_Bri)
	on_state = True
	color_state = False
	dim_state = False
	setStateLabel('The lights are set to ON')
	return;

def setLightsCOLOR():
	global on_state
	global color_state
	global dim_state
	lights[1].on = False
	#setLight(1, True, color_Hue_1, color_Sat_1, color_Bri_1)
	setLight(2, True, color_Hue_2, color_Sat_2, color_Bri_2)
	setLight(3, True, color_Hue_3, color_Sat_3, color_Bri_3)
	on_state = False
	color_state = True
	dim_state = False
	setStateLabel('The lights are set to COLOR')
	return;

def setLightsDIM():
	global on_state
	global color_state
	global dim_state
	lights[1].on = False
	#setLight(1, True, dim_Hue, dim_Sat, dim_Bri)
	setLight(2, True, dim_Hue, dim_Sat, dim_Bri)
	lights[3].on = False
	#setLight(3, True, dim_Hue, dim_Sat, dim_Bri)
	on_state = False
	color_state = False
	dim_state = True
	setStateLabel('The lights are set to DIM')
	return;

def setStateLabel(text_str):
	#screen.fill(pygame.Color("black"))	#erase screen
	#font = pygame.font.Font(None, 25)	#set font parameters
	#label_text = font.render(str(text_str), True, (255,255,255))	#assign text, make visible, make color white
	#screen.blit(label_text, (0,10))		#set label position
	#pygame.display.update()			#update the screen
	print text_str
	return;

#code to check if lights were in not-off state when program started
#b.get_light(1, 'hue')
if(lights[2].hue == on_Hue):
	on_state = True
	color_state = False
	dim_state = False
	state_text = 'The lights are set to ON'
elif(lights[2].hue == color_Hue_2):
	on_state = False
	color_state = True
	dim_state = False
	state_text = 'The lights are set to COLOR'
elif(lights[2].hue == dim_Hue):
	on_state = False
	color_state = False
	dim_state = True
	state_text = 'The lights are set to DIM'
else:
	state_text = 'The lights are OFF'

setStateLabel(state_text)


while True:
    try:
  #set loop active line in state file - indicates main loop is running
	state_data[0] = str(time())
	state_data[3] = 'loop_active'
	#write to file
	writeStateFile(state_data)
	#key press handler using pygame events
	#for event in pygame.event.get():
		#if event.type == pygame.KEYDOWN:
			#if event.key == pygame.K_SPACE:
				#allOff()
			#q key turns on full brightness
			#if event.key == pygame.K_q:
				#if(on_state == False):
					#setLightsON()
				#else:
					#allOff()
			#a key turns lights on color mode
			#if event.key == pygame.K_a:
				#if(color_state == False):
					#setLightsCOLOR()
				#else:
					#allOff()
			#z key turn lights on in dim mode
			#if event.key == pygame.K_z:
				#if(dim_state == False):
					#setLightsDIM()
				#else:
					#allOff()
        #if "ON" button pressed but not held and no other buttons were pressed - then set lights to "ON" profile
	if(GPIO.input(ON_PIN) == False and buttonHeld(ON_PIN) == False and GPIO.input(COLOR_PIN) == True and GPIO.input(DIM_PIN) == True):
           #if this light combo is not already on then turn it on
           if(on_state == False):       
		setLightsON()
		#setAll(True, on_Hue, on_Sat, on_Bri)
	        #on_state = True
	        #color_state = False
                #dim_state = False
           #otherwise turn everything off
           else:
               allOff()
        #if "COLOR" button pressed but not held and no other buttons were pressed - then set lights to "COLOR" profile
        if(GPIO.input(COLOR_PIN) == False and buttonHeld(COLOR_PIN) == False and GPIO.input(ON_PIN) == True and GPIO.input(DIM_PIN) == True):
           #if this light combo is not already on then turn it on
           if(color_state == False):
		setLightsCOLOR()
		#setLight(1,True, color_Hue_1, color_Sat_1, color_Bri_1)
	        #setLight(2,True, color_Hue_2, color_Sat_2, color_Bri_2)
	        #setLight(3,True, color_Hue_3, color_Sat_3, color_Bri_3)
                #on_state = False
                #color_state = True
                #dim_state = False
           #otherwise turn everything off
           else:
               allOff()
        #if "DIM" button pressed but not held and no other buttons were presed -  then set lights to "DIM" profile
        if(GPIO.input(DIM_PIN) == False and buttonHeld(DIM_PIN) == False and GPIO.input(ON_PIN) == True and GPIO.input(COLOR_PIN) == True):
            #if this light combo is not already on then turn it on
            if(dim_state == False):
                setLightsDIM()
		#setAll(True, dim_Hue, dim_Sat, dim_Bri)
	        #on_state = False
                #color_state = False
                #dim_state = True
            #otherwise turn everything off
            else:
               allOff()
        if(GPIO.input(ON_PIN) == False and GPIO.input(COLOR_PIN) == False and GPIO.input(DIM_PIN) == False):
		break
	sleep(.1);
    except KeyboardInterrupt:
	break

#shut off all LEDS before terminating    
#GPIO.output(ON_LED, False)
#GPIO.output(COLOR_LED, False)
#GPIO.output(DIM_LED, False)

#initialize state data array
state_data[0] = str(time())
state_data[1] = 'script_terminated'
state_data[2] = 'bridge_disconnected'
state_data[3] = 'loop_terminated'
#write to file
writeStateFile(state_data)

print "switch.py terminated..."

