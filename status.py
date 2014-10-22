#!/usr/bin/env python

#Written by Nicholas Mykulowycz
#Created on Oct 15, 2014
#script for checking status of switch.py script

import os
import sys
from time import time
from time import sleep
from time import ctime
import RPi.GPIO as GPIO
from subprocess import call
import pickle   #for saving/reading variables to/from file
import smtplib	#for email notifications

running = True
MAX_TIME = float(3) # 3 seconds is the max time a file write is considered valid
GMAIL_USER = 'bot4756@gmail.com'
GMAIL_PASS = 'thesewords1'
recipient = 'nanosecrepair@gmail.com'
subject = 'HeavySwitch has taken its own life'
mail_host = 'smtp.gmail.com:587'
#header for email
headers = "\r\n".join(["from: " + GMAIL_USER,
                       "subject: " + subject,
                       "to: " + recipient,
                       "mime-version: 1.0",
                       "content-type: text/html"])

#booleans
started = False
connected = False
looping = False

error_count = 0
last_email_sent = 0
state_array =['0', 'script_terminated', 'bridge_disconnected', 'loop_terminated']

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

print "status.py running..."
print "Press CTRL+C to terminate script\n"

while running:
  try:
    #make sure file exists before un pickling
    if os.path.getsize('log/state') > 0:
    	#open the pickled file
    	with open('log/state', 'r') as fileObj:
    	  #de-pickle the file
    	  state_array = pickle.load(fileObj)
    #pull the timestamp the pickling occured
    file_time = float(state_array[0])
  
    #check current time
    curr_time = time()

    #print "file time was:   %f" % file_time
    #print "current time is: %f" % curr_time

    #print error_count

    diff_time = curr_time-file_time

    #check the timespamp to ensure the last write was recent
    if(diff_time < MAX_TIME):
    
      #check if the script started
      if(state_array[1] == 'script_started'):
        #set all first LED to on - indicates script ran
        GPIO.output(ON_LED, True)
	started = True
      else:
        GPIO.output(ON_LED, False)
	started = False
	error_count += 1
      
      #check if bridge connection was established
      if(state_array[2] == 'bridge_connected'):
        #set second LED to on - indicates bridge connection was set up
        GPIO.output(COLOR_LED, True)
	connected = True
      else:
        GPIO.output(COLOR_LED, False)
	connected = False
	error_count += 1

      #check if main loop is acive
      if(state_array[3] == 'loop_active'):
        #the third LED is on - indicates the main loop was reached
        GPIO.output(DIM_LED, True)
	looping = True
      else:
        GPIO.output(DIM_LED, False)
	looping = False
	error_count += 1
	
  
    #if time value too old turn off all LEDs  
    else:
      GPIO.output(ON_LED, False)
      GPIO.output(COLOR_LED, False)
      GPIO.output(DIM_LED, False)
      error_count += 1

    #if more than 120 errors have occured then send an email
    if(error_count > 120):
      #check that an email has not been sent in over a day before sending another
      if(curr_time > (last_email_sent+86400)):
        body_of_email  = "We regret to inform you that your HeavySwitch encountered some sort of error and decided the best course of action would be to end its life*"
        body_of_email += "\n\n* There is no evidence to substantiate this claim and/or prove it is not entirely made it up."
        body_of_email += "\n\nCurrent Timestamp: %s" % ctime(time())
        body_of_email += "\nLast File Timestamp: %s" % ctime(float(state_array[0]))
        body_of_email += "\nAttribute 1: %s" % state_array[1]
        body_of_email += "\nAttribute 2: %s" % state_array[2]
        body_of_email += "\nAttribute 3: %s" % state_array[3]
        body_of_email += "\nNumber of Errors: %d" % error_count
        print '\n' + body_of_email
        #replace new lines with br elements to properly format for gmail
        body_of_email = body_of_email.replace('\n', '<br />')
        content = headers + "\r\n\r\n" + body_of_email
      
        #log into gmail
        session = smtplib.SMTP(mail_host)
        session.ehlo()
        session.starttls()
        session.login(GMAIL_USER,GMAIL_PASS)
        #send the email
        session.sendmail(GMAIL_USER, recipient, content)
        session.quit()
        #set timestamp the email was sent at to avoid spamming my inbox
        last_email_sent = time()

    #reset error counter if everything is functioning normally and timestamps have not expired
    if((started == True and connected == True and looping == True) and diff_time< MAX_TIME):    
      error_count = 0

    #loop executes once every 500ms
    sleep(.5)
  except KeyboardInterrupt:
    break


#shut off all LEDS before terminating
GPIO.output(ON_LED, False)
GPIO.output(COLOR_LED, False)
GPIO.output(DIM_LED, False)

print "status.py terminated..."
