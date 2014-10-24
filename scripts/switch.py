#!/usr/bin/env python

#Written by Nicholas Mykulowycz
#Created on May 25, 2014
#script for reading button inputs and sending commands to lights

import os
import sys
#import pygame
#from pygame.locals import *
import curses
from time import sleep
from time import time
from phue import Bridge
import RPi.GPIO as GPIO
from subprocess import call
import pickle   #for saving/reading variables to/from file
#import threading #for handling key press events with out tying up the script

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

def updateScreen():
	global light_str
	global state_data
	time_string = ctime(time())
	# print current light state
	term.addstr(1,1, ("The lights were set to %s as of %s" % (light_str,time_string)))
	# print data from state array
	term.addstr(3,1, ("Timestamp: %s" % state_data[0]))
	term.addstr(4,1, ("1: %s" % state_data[1]))
	term.addstr(5,1, ("2: %s" % state_data[2]))
	term.addstr(6,1, ("3: %s" % state_data[3]))
	return;

#switch status booleans
on_state = False
color_state = False
dim_state = False
light_str = "OFF"

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

#initialize curses
term = curses.initscr()
curses.cbreak()	#turns off line buffering
curses.noecho() #turns of echo in terminal
term.nodelay(True)	#makes curse getch non blocking

b = Bridge(BRIDGE_IP)
lights = b.get_light_objects('id')

#set bridge_connected line in state file - indicates bridge connection was set up
state_data[0] = str(time())
state_data[2] = 'bridge_connected'
#write to file
writeStateFile(state_data)
updateScreen()

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
    global light_str
    lights[1].on = False
    lights[2].on = False
    lights[3].on = False
    on_state = False
    color_state = False
    dim_state = False
    light_str = "OFF"
    updateScreen()
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
	global light_str
	setAll(True, on_Hue, on_Sat, on_Bri)
	on_state = True
	color_state = False
	dim_state = False
	light_str = "ON"
	updateScreen()
	return;

def setLightsCOLOR():
	global on_state
	global color_state
	global dim_state
	global light_str
	lights[1].on = False
	#setLight(1, True, color_Hue_1, color_Sat_1, color_Bri_1)
	setLight(2, True, color_Hue_2, color_Sat_2, color_Bri_2)
	setLight(3, True, color_Hue_3, color_Sat_3, color_Bri_3)
	on_state = False
	color_state = True
	dim_state = False
	light_str = "COLOR"
	updateScreen()
	return;

def setLightsDIM():
	global on_state
	global color_state
	global dim_state
	global light_str
	lights[1].on = False
	#setLight(1, True, dim_Hue, dim_Sat, dim_Bri)
	setLight(2, True, dim_Hue, dim_Sat, dim_Bri)
	lights[3].on = False
	#setLight(3, True, dim_Hue, dim_Sat, dim_Bri)
	on_state = False
	color_state = False
	dim_state = True
	light_str = "DIM"
	updateScreen()
	return;



#code to check if lights were in not-off state when program started
#b.get_light(1, 'hue')
if(lights[2].hue == on_Hue):
	on_state = True
	color_state = False
	dim_state = False
	light_str = 'ON'
elif(lights[2].hue == color_Hue_2):
	on_state = False
	color_state = True
	dim_state = False
	light_str = 'COLOR'
elif(lights[2].hue == dim_Hue):
	on_state = False
	color_state = False
	dim_state = True
	light_str = 'DIM'
elif(lighs[1].on == False and lights[2].on == False and lights[3].on == False):
	light_str = 'OFF'
else:
	light_str = 'UNKNOWN'


while True:
    try:
  #set loop active line in state file - indicates main loop is running
	state_data[0] = str(time())
	state_data[3] = 'loop_active'
	#write to file
	writeStateFile(state_data)
	updateScreen()
	#key press handler using curses
	key = term.getch()
	# key = -1 if there was no key detected
	if(key != -1):
		# if 'SPACE' key was pressed
		if(str(key) == ' '):
			allOff()
		# if 'Q' key was presed - set to ON
		elif(str(key) == 'q' or str(key) == 'Q'):
			if(on_state == False):
				setLightsON()
			else:
				allOff()
		# if 'A' key was pressed - set to COLOR
		elif(str(key) == 'a' or str(key) == 'A'):
			if(color_state == False):
				setLightsCOLOR()
			else:
				allOff()
		# if 'Z' key was pressed - set to DIM
		elif(str(key) == 'z' or str(key) == 'Z'):
			if(dim_state == False):
				setLightsDIM()
			else:
				allOff()

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
	sleep(.05);
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

# turn back on echo
curses.echo()

print "switch.py terminated..."

