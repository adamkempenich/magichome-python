# MagicHome-Python API
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
      (Higher numbers reserved for future use)

   Functions accept integers 0-255 as parameters.
   
To create a new instance of the API, use the following terminology:
`My_New_API = MagicHome_Wifi_Api([IP Address],[Device Type (from above)])`
And then call its functions in the following manner:
To turn a device on:
`My_New_API.On`
And similarly, to turn it off:
`My_New_API.Off`
To update a colored device, send R,G, and B to it.
`My_New_API.Update_Device(R,G,B)`
And if that device supports WW/CW (or both):
`My_New_API.Update_Device(R,G,B,WW,CW)`
BUT, if you want to update a bulb's white level, send R,G,B AND W... only W's level will be used.
`My_New_API.Update_Device(R,G,B,W)`
To Update a Bulb's color, you don't need to send the W parameter.
Finally, to send a preset command:
`My_New_API.Send_Preset_Function(25, 100)`
Presets can range from 0x25 (int 37) to 0x38 (int 56), anything outside of this will be rounded up or down.
A speed of 100% is fastest, and 0% is super duper slow.
