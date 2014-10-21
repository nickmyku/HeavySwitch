#!/usr/bin/env python

#Written by Nicholas Mykulowycz
#Created on Oct 15, 2014
#script for checking status of switch.py script

import os
import sys
from time import time
from time import sleep
import pickle   #for saving/reading variables to/from file

running = True
MAX_TIME = 1

#pin definitions
ON_LED = 27
DIM_LED = 22
COLOR_LED = 17

#configure pins
GPIO.setwarnings(False)		#silence pin in use warning
GPIO.setmode(GPIO.BCM)
GPIO.setup(ON_LED, GPIO.OUT)
GPIO.setup(DIM_LED, GPIO.OUT)
GPIO.setup(COLOR_LED, GPIO.OUT)

while running:
  #open the state file and read the data
  #with open('log/state', 'r') as f:
  #  read_data = f.read()
  #then imediately close the file
  #f.closed
  #split the text into array elements with whitespace delimiters
  #info = read_data.split()
  
  #convert time string into number
  #file_time = int(info[0])
  
  #open the pickled file
  fileObj = open('log/state', 'r')
  #de-pickle the file
  state_array = pickle.load(fileObj)
  #pull the timestamp the pickling occured
  file_time = state_array[0]
  
  #check current time
  curr_time = time()

  #check the timespamp to ensure the last write was recent
  if((curr_time-file_time) < MAX_TIME):
    
    #check if the script started
    if(state_array[1] == 'script_started'):
      #set all first LED to on - indicates script ran
      GPIO.output(ON_LED, True)
    else:
      GPIO.output(ON_LED, False)
      
    #check if bridge connection was established
    if(state_array[2] == 'bridge_connected'):
      #set second LED to on - indicates bridge connection was set up
      GPIO.output(COLOR_LED, True)
    else:
      GPIO.output(COLOR_LED, False)

    #check if main loop is acive
    if(state_array[3] == 'loop_active'):
      #the third LED is on - indicates the main loop was reached
      GPIO.output(DIM_LED, True)
    else:
      GPIO.output(DIM_LED, False)
  
  #if time value too old turn off all LEDs  
  else:
    GPIO.output(ON_LED, False)
    GPIO.output(COLOR_LED, False)
    GPIO.output(DIM_LED, False)
    
  #loop executes once every 500ms
  sleep(.5)


#shut off all LEDS before terminating
GPIO.output(ON_LED, False)
GPIO.output(COLOR_LED, False)
GPIO.output(DIM_LED, False)
