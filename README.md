# magichome-python
MagicHome Wifi protocol for python.

Copyright 2016, Adam Kempenich. Questions? Comments? Feedback of any kind? Find me on GITHUB, @AdamKempenich
This utility was designed for use with devices compatible with the MagicHome Wifi app. 

It currently supports:
  * Bulbs (Firmware v.4 and greater)
  * Legacy Bulbs (Firmware v.3 and lower)
  * RGB Controllers
  * RGB+WW Controllers
  * RGB+WW+CW Controllers

##### Commands:
  * Turning devices on and off
  * Getting current device states
  * Setting either colors, or whites (in bulbs)
  * Setting colors (+ WW + CW) in compatible devices
  * Sending preset functions

	
##### Tasks:
  * Initial device setup via UDP.
  * Custom commands (I know how it works ... just not a priority to implement currently.)
  * Setting the device's internal clock.

##### Notes:
   Device types are:
  *    0: RGB
  *    1: RGB+WW
  *    2: RGB+WW+CW
  *    3: Bulb (v.4+)
  *    4: Bulb (v.3-)
  *    (Higher numbers reserved for future use)

   Functions accept integers 0-255 as parameters, or their equivalent byte format.
