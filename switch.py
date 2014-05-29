#!/usr/bin/env python

import time
import sys
import RPi.GPIO as GPIO
from time import sleep
from phue import Bridge
from subprocess import call

b = Bridge('192.168.1.11')
lights = b.get_light_objects('id')

hold_time = .6   #amount of time in seconds which must pass for a button to register a hold

#pin definitions
ON_PIN = 23
COLOR_PIN = 24
DIM_PIN = 25

#350
#on light parameters
on_Hue = 35000		#hue value, from 0 to 65280
on_Sat = 255		#saturation value, from 0 to 255, higher the more colorful
on_Bri = 255		#brightness value, from 0 to 255, higher is brighter

#color light parameters
color_Hue_1 = 58000	#hue value, from 0 to 65280
color_Sat_1 = 255	#saturation value, from 0 to 255, higher the more colorful
color_Bri_1 = 127		#brightness value, from 0 to 255, higher is brighter
color_Hue_2 = 47000	#hue value, from 0 to 65280
color_Sat_2 = 255	#saturation value, from 0 to 255, higher the more colorful
color_Bri_2 = 200	#brightness value, from 0 to 255, higher is brighter
color_Hue_3 = 58000	#hue value, from 0 to 65280
color_Sat_3 = 255	#saturation value, from 0 to 255, higher the more colorful
color_Bri_3 = 127		#brightness value, from 0 to 255, higher is brighter

#dim light parameters
dim_Hue = 10000		#hue value, from 0 to 65280
dim_Sat = 100		#saturation value, from 0 to 255, higher the more colorful
dim_Bri = 1		#brightness value, from 0 to 255, higher is brighter

GPIO.setmode(GPIO.BCM)
GPIO.setup(ON_PIN, GPIO.IN)     #full om input pin
GPIO.setup(COLOR_PIN, GPIO.IN)     #color on input pin
GPIO.setup(DIM_PIN, GPIO.IN)     #dim on input pin

def setLight(light_num, on_val, hue_val, sat_val, bright_val):
    lights[light_num].on = on_val
    lights[light_num].hue = hue_val
    lights[light_num].saturation = sat_val
    lights[light_num].brightness = bright_val
    return;


def allOff():
    lights[1].on = False
    lights[2].on = False
    lights[3].on = False
    return;

def setAll(on_val, hue_val, sat_val, bright_val):
    setLight(1, on_val, hue_val, sat_val, bright_val)
    setLight(2, on_val, hue_val, sat_val, bright_val)
    setLight(3, on_val, hue_val, sat_val, bright_val)
    return;

def buttonHeld(pin):
    start_time = time.time()
    curr_time = time.time()

    #loop continues while time elapsed is less than the hold time threashold
    #and the button is still being held
    while((curr_time-start_time < hold_time) and GPIO.input(pin) == False):
        sleep(0.05);
        curr_time = time.time()

    #if pin is still held after loop exits button hold detected
    #turn off all lights and return true
    if(GPIO.input(pin) == False):
        allOff()
        sleep(2)
        return True;
    #if button was released then it was not held return false
    else:
        return False;


print("\npress Ctrl+C to terminate script")

while True:
    try:
        if(GPIO.input(ON_PIN) == False and buttonHeld(ON_PIN) == False):
            setAll(True, on_Hue, on_Sat, on_Bri)
        
        if(GPIO.input(COLOR_PIN) == False and buttonHeld(COLOR_PIN) == False):
            setLight(1,True, color_Hue_1, color_Sat_1, color_Bri_1)
	    setLight(2,True, color_Hue_2, color_Sat_2, color_Bri_2)
	    setLight(3,True, color_Hue_3, color_Sat_3, color_Bri_3)
        
        if(GPIO.input(DIM_PIN) == False and buttonHeld(DIM_PIN) == False):
            setAll(True, dim_Hue, dim_Sat, dim_Bri)
        sleep(.1);
    except KeyboardInterrupt:
	break
    



