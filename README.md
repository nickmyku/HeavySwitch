HeavySwitch
===========

brains behind the world's most over complicated light switch

This script is running on a Raspberry Pi stuffed in my closet that is connected to a wall mounted light switch. The script interprets buttons presses and sends commands through the ethernet port to the Philips Hue bridge. the bridge then communicates the commands to the Philips Hue wireless lightbulbs in my bedroom.

A more complete write up/explaination can be found on my blog - electric campfire:

http://electriccampfire.info/2014/06/12/over-complicating-a-light-switch/

3 momentary push buttons are used as inputs, they are pulled high using an add on board.

each switch has a LED to illuminate it, these LEDs are used to locate the lightswitch in the dark and to indicate the programs status.

ALL LEDS OFF - script failed to start or exited safely

FIRST LED ON - script started, defined global varibles, and output pins

SECOND LED ON - connection to hue bridge has been established

THIRD LED ON - the script made it to the main loop (but the main loop is not necessarily running still)

