#!/usr/bin/env python

import time
import sys
import RPi.GPIO as GPIO
from time import sleep
from phue import Bridge
from subprocess import call

hold_time = .6   #amount of time in seconds which must pass for a button to register a hold

#pin definitions
ON_PIN = 24
COLOR_PIN = 23
DIM_PIN = 25
ON_LED = 27
DIM_LED = 22
COLOR_LED = 17

#switch status booleans
on_state = False
color_state = False
dim_state = False

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
GPIO.setup(ON_LED, GPIO.OUT)
GPIO.setup(DIM_LED, GPIO.OUT)
GPIO.setup(COLOR_LED, GPIO.OUT)

#set all first LED to on - indicates script ran
GPIO.output(ON_LED, True)

b = Bridge('192.168.1.202')
lights = b.get_light_objects('id')

#set second LED to on - indicates bridge connection was set up
GPIO.output(COLOR_LED, True)

def setLight(light_num, on_val, hue_val, sat_val, bright_val):
    lights[light_num].on = on_val
    lights[light_num].hue = hue_val
    lights[light_num].saturation = sat_val
    lights[light_num].brightness = bright_val
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
    return;

def setAll(on_val, hue_val, sat_val, bright_val):
    setLight(1, on_val, hue_val, sat_val, bright_val)
    setLight(2, on_val, hue_val, sat_val, bright_val)
    setLight(3, on_val, hue_val, sat_val, bright_val)
    return;

def buttonHeld(pin):
    start_time = time.time()
    curr_time = time.time()
    
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
    while((curr_time-start_time < hold_time) and GPIO.input(pin) == False and GPIO.input(alt_pin_1) == True and GPIO.input(alt_pin_2) == True):
        sleep(0.05);
        curr_time = time.time()

    #if pin is still held after loop exits button hold detected AND no other buttons are pressed
    #turn off all lights and return true
    if(GPIO.input(pin) == False and GPIO.input(alt_pin_1) == True and GPIO.input(alt_pin_2) == True):
        allOff()
        sleep(2)
        return True;
    #if button was released then it was not held return false
    else:
        return False;


print("\npress Ctrl+C or press all buttons to terminate script")

#set third LED to on - indicates main loop was reached
GPIO.output(DIM_LED, True)

while True:
    try:
        #if "ON" button pressed but not held and no other buttons were pressed - then set lights to "ON" profile
	if(GPIO.input(ON_PIN) == False and buttonHeld(ON_PIN) == False and GPIO.input(COLOR_PIN) == True and GPIO.input(DIM_PIN) == True):
           #if this light combo is not already on then turn it on
           if(on_state == False):       
               setAll(True, on_Hue, on_Sat, on_Bri)
	       on_state = True
	       color_state = False
               dim_state = False
           #otherwise turn everything off
           else:
               allOff()
        #if "COLOR" button pressed but not held and no other buttons were pressed - then set lights to "COLOR" profile
        if(GPIO.input(COLOR_PIN) == False and buttonHeld(COLOR_PIN) == False and GPIO.input(ON_PIN) == True and GPIO.input(DIM_PIN) == True):
           #if this light combo is not already on then turn it on
           if(color_state == False):
               setLight(1,True, color_Hue_1, color_Sat_1, color_Bri_1)
	       setLight(2,True, color_Hue_2, color_Sat_2, color_Bri_2)
	       setLight(3,True, color_Hue_3, color_Sat_3, color_Bri_3)
               on_state = False
               color_state = True
               dim_state = False
           #otherwise turn everything off
           else:
               allOff()
        #if "DIM" button pressed but not held and no other buttons were presed -  then set lights to "DIM" profile
        if(GPIO.input(DIM_PIN) == False and buttonHeld(DIM_PIN) == False and GPIO.input(ON_PIN) == True and GPIO.input(COLOR_PIN) == True):
            #if this light combo is not already on then turn it on
            if(dim_state == False):
               setAll(True, dim_Hue, dim_Sat, dim_Bri)
	       on_state = False
               color_state = False
               dim_state = True
            #otherwise turn everything off
            else:
               allOff()
        if(GPIO.input(ON_PIN) == False and GPIO.input(COLOR_PIN) == False and GPIO.input(DIM_PIN) == False):
		break
	sleep(.1);
    except KeyboardInterrupt:
	break
    
GPIO.output(ON_LED, False)
GPIO.output(COLOR_LED, False)
GPIO.output(DIM_LED, False)


