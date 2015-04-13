#!/usr/bin/env python

#Written by Nicholas Mykulowycz
#Created on Oct 22, 2014
#script for sending a notification email when the pi powers on

import os
import sys
from time import time
from time import ctime
import smtplib	#for email notifications

#load shared global variables
#execfile('/home/pi/HeavySwitch/scripts/shared_globals.py')
execfile('scripts/shared_globals.py')

# subject of email
subject = 'HeavySwitch has been reborn! rejoice!'
# header for email
headers = "\r\n".join(["from: " + GMAIL_USER,
                       "subject: " + subject,
                       "to: " + recipient,
                       "mime-version: 1.0",
                       "content-type: text/html"])

# construct the message
body_of_email  = "We thought for sure your HeavySwitch was dead, it showed all the tell tale signs of rigor mortis. "
body_of_email += "But against all odds it has been given new life and once again walks amongst us mortals *"
body_of_email += "We cannot find a logical scientific theory to explain this phenomenon and have come to the conclusion "
body_of_email += "that your HeavySwitch is a witch and/or is working with the devil."
body_of_email += "At your earliest convenience would you kindly burn the HeavySwitch at the stake "
body_of_email += "to ensure its devil worship is not spread."
body_of_email += "\n\n* The HeavySwitch has no legs and is therefore not capable of walking."
body_of_email += "\n\nYour friendly psychopathic notification bot,"
body_of_email += "\n-Bot4756"
body_of_email += "\n\nCurrent Timestamp: %s" % ctime(time())
print '\n' + body_of_email
# replace new lines with br elements to properly format for gmail
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
