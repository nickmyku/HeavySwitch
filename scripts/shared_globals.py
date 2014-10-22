# set path for state file
STATE_PATH = '/home/pi/HeavySwitch/log/state'
# amount of time button needs to be held for it to be considered a 'long' press
HOLD_TIME = .6
# 5 seconds is the max time a file write is considered valid
MAX_TIME = 5 #float(5)
# number of consecutive errors which must occure before error email is sent
MAX_ERRORS = 120 # 120 is approx one minute delay


# email credientials
GMAIL_USER = 'bot4756@gmail.com'
GMAIL_PASS = 'thesewords1'
recipient = 'nanosecrepair@gmail.com'
mail_host = 'smtp.gmail.com:587'


# input pin definitions
ON_PIN = 24
COLOR_PIN = 23
DIM_PIN = 25
# led pin definitions
ON_LED = 27
DIM_LED = 22
COLOR_LED = 17


# on light parameters
on_Hue = 35000		#hue value, from 0 to 65280
on_Sat = 255		#saturation value, from 0 to 255, higher the more colorful
on_Bri = 255		#brightness value, from 0 to 255, higher is brighter
# color light parameters
color_Hue_1 = 58000	#hue value, from 0 to 65280
color_Sat_1 = 255	#saturation value, from 0 to 255, higher the more colorful
color_Bri_1 = 127		#brightness value, from 0 to 255, higher is brighter
color_Hue_2 = 47000	#hue value, from 0 to 65280
color_Sat_2 = 255	#saturation value, from 0 to 255, higher the more colorful
color_Bri_2 = 200	#brightness value, from 0 to 255, higher is brighter
color_Hue_3 = 58000	#hue value, from 0 to 65280
color_Sat_3 = 255	#saturation value, from 0 to 255, higher the more colorful
color_Bri_3 = 127		#brightness value, from 0 to 255, higher is brighter
# dim light parameters
dim_Hue = 10000		#hue value, from 0 to 65280
dim_Sat = 100		#saturation value, from 0 to 255, higher the more colorful
dim_Bri = 1		#brightness value, from 0 to 255, higher is brighter

