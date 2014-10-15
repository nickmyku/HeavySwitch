#!/usr/bin/env python

#Written by Nicholas Mykulowycz
#Created on Oct 15, 2014
#script for checking status of switch.py script

import os
import sys
import time
from time import sleep

#pin definitions
ON_LED = 27
DIM_LED = 22
COLOR_LED = 17

#configure pins
GPIO.setwarnings(False)		#silence pin in use warning
GPIO.setup(ON_LED, GPIO.OUT)
GPIO.setup(DIM_LED, GPIO.OUT)
GPIO.setup(COLOR_LED, GPIO.OUT)

#set all first LED to on - indicates script ran
GPIO.output(ON_LED, True)

#set second LED to on - indicates bridge connection was set up
GPIO.output(COLOR_LED, True)

#the third LED is on - indicates the main loop was reached
GPIO.output(DIM_LED, True)
