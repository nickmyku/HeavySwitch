HeavySwitch
===========

brains behind the world's most over complicated light switch

###Background Info

This script is running on a Raspberry Pi stuffed in my closet that is connected to a wall mounted light switch. The script interprets buttons presses and sends commands through the ethernet port to the Philips Hue bridge. the bridge then communicates the commands to the Philips Hue wireless lightbulbs in my bedroom.

A more complete write up/explaination can be found on my blog - [Electric Campfire](http://electriccampfire.info/2014/06/12/over-complicating-a-light-switch/)

###Wiring Info

3 momentary push buttons are used as inputs, they are pulled high using a custom add on board, pressing the switch overpowers the pull up resistors and creates a logic low on the input pin.

each switch has a LED to illuminate it, these LEDs are used to locate the lightswitch in the dark and to indicate the program's status.

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

###Notes

1. Make sure to change the bridge ip address to reflect that of the one on your network.
