HeavySwitch
===========

brains behind the world's most over complicated light switch

###Background Info

This script is running on a Raspberry Pi stuffed in my closet that is connected to a wall mounted light switch. The script interprets buttons presses and sends commands through the ethernet port to the Philips Hue bridge. the bridge then communicates the commands to the Philips Hue wireless lightbulbs in my bedroom.

A more complete write up/explaination can be found on my blog - [Electric Campfire](http://electriccampfire.info/2014/06/12/over-complicating-a-light-switch/)

###Wiring Info

3 momentary push buttons are used as inputs, they are pulled high using a custom add on board, pressing the switch overpowers the pull up resistors and creates a logic low on the input pin.

each switch has a LED to illuminate it, these LEDs are used to locate the lightswitch in the dark and to indicate the program's status.

###Script Structure

The program has been broken into two parts. One part actually controls the lights and monitors the physical switches (switch.py). The other part monitors the switch application to make sure it is working (status.py) and sends a notification email if it detects a fault. The pickle module is used to 'communicate' between the two programs by serializing and deserializing an array varible that is structured in the following way:

| Element # | Description | Possible Values |
| :-------: | :---------: | :----: |
| 0 | timestamp of last write | x.xx |
| 1 | is the script running? | 'script_terminated', 'script_started' |
| 2 | is the bridge connected? | 'bridge_disconnected', 'bridge_connected' |
| 3 | is the switch.py main loop running? | 'loop_terminated', 'loop_running' |

###LED Status 

| LED STATE | EXPLAINATION |
| :---------: | :------------ |
| ALL LEDS OFF | Script failed to start or exited safely |
| FIRST LED ON | Script started, defined global varibles, and set IO pin states |
| SECOND LED ON | Connection to hue bridge has been established |
| THIRD LED ON | The script made it to the main loop (but the main loop is not necessarily running still) |

###Button Functions

|  BUTTON  |   INTERACTION   | RESULT |
| :------: | :-------------: | :----- |
| First Button | First Short  Press | All 3 lights are turned on to full intensity cool white |
| First Button | Second Short Press | If lights are still on and in the full intensty cool white state pressing the button again will turn them off
| First Button | Long Press | Turn off any lights that are currently on |
| Second Button | First Short  Press | All 3 lights are turned on to a medium intensity pink or cyan |
| Second Button | Second Short Press | If lights are still on and in the medium intensity pink or cyan state pressing the button again will turn them off
| Second Button | Long Press | Turn off any lights that are currently on |
| Third Button | First Short  Press | All 3 lights are turned on to low intensity warm white |
| Third Button | Second Short Press | If lights are still on and in the low intensty warm white state pressing the button again will turn them off
| Third Button | Long Press | Turn off any lights that are currently on |
| All Three Buttons | Short Press | Terminate script - implemented for debuging using ssh |

###Keyboard Functions

Keyboard key functionality was added to control the lights remotely using a bluetooth keyboard

|  KEY  |   INTERACTION   | RESULT |
| :------: | :-------------: | :----- |
| 'Q' | First Press | All 3 lights are turned on to full intensity cool white |
| 'Q' | Second Press | All 3 lights are turned off |
| 'A' | First Press | All 3 lights are turned on to a medium intensity pink or cyan |
| 'A' | Second Press | All 3 lights are turned off |
| 'Z' | First Press | All 3 lights are turned on to low intensity warm white |
| 'Z' | Second Press | All 3 lights are turned off |
| SPACEBAR | Any Press | Terminate script - implemented for debuging using ssh |

###Other

By utilizing the pygame library now any screen connected to the pi will show the state of the lights, and plain text messages are sent through any ssh connection

* pygame lib has been disabled until I can fix the start up issues with it


###Notes

1. Make sure to change the bridge ip address to reflect that of the one on your network.
2. Also remember to hit the sync button on the Bridge the first time the script runs to authenticate it.
