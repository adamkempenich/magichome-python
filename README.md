# MagicHome-Python API
MagicHome Wifi protocol for Python.

This utility was designed for use with devices compatible with the MagicHome Wifi app.

### This project is inactive and I am not working on it. I will gladly review and merge pull requests, though!

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
* 0: RGB
* 1: RGB+WW
* 2: RGB+WW+CW
* 3: Bulb (v.4+)
* 4: Bulb (v.3-)
  (Higher numbers reserved for future use)

Functions accept integers 0-255 as parameters.

To create a new instance of the API, use the following terminology:

```python
controller1 = MagicHomeApi('IP Address', [Device Type (from above)])
```

And then call its functions in the following manner:

Get the status of a device:

```python
controller1.get_status()
```

To turn a device on:

```python
controller1.turn_on
```

And similarly, to turn it off:

```python
controller1.turn_off
```

To update a colored device, send R, G, and B to it.

```python
controller1.update_device(R, G, B)
```

And if that device supports WW/CW (or both):

```python
controller1.update_device(R, G, B, WW, CW)
```

BUT, if you want to update a bulb's white level, send R,G,B AND W... only W's level will be used.

```python
controller1.update_device(R, G, B, W)
```

To Update a Bulb's color, you don't need to send the W parameter.
Finally, to send a preset command:

```python
controller1.send_preset_function(25, 100)
```

Presets can range from 0x25 (int 37) to 0x38 (int 56), anything outside of this will be rounded up or down.

A speed of 10 0% is fastest, and 0 % is super duper slow.

Copyright 2016 Adam Kempenich. Licensed under MIT.

Questions? Comments? Feedback of any kind? Find me on Github, @AdamKempenich
