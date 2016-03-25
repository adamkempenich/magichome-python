#!/usr/bin/env python

"""
Copyright 2016, Adam Kempenich. Questions? Comments? Feedback of any kind? Find me on GITHUB, @AdamKempenich
This utility was designed for use with devices compatible with the MagicHome Wifi app. 

It currently supports:
   Bulbs (Firmware v.4 and greater)
   Legacy Bulbs (Firmware v.3 and lower)
   RGB Controllers
   RGB+WW Controllers
   RGB+WW+CW Controllers

##### Commands:
   Turning devices on and off
   Getting current device states
   Setting either colors, or whites (in bulbs)
   Setting colors (+ WW + CW) in compatible devices
   Sending preset functions

	
##### Tasks:
   Initial device setup via UDP.
   Custom commands (I know how it works ... just not a priority to implement currently.)
   Setting the device's internal clock.

##### Notes:
   Device types are:
      0: RGB
      1: RGB+WW
      2: RGB+WW+CW
      3: Bulb (v.4+)
      4: Bulb (v.3-)
      (Higher numbers reserved for future use)

   Functions accept integers 0-255 as parameters, or their equivalent byte format.

"""

import socket, csv, struct

class Api:   
   def __init__(self, device_ip, device_type):
      self.device_ip = device_ip
      self.device_type = device_type
      self.API_PORT = 5577
      self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

   def On(self):
      #Turns a device on
      self.Send_Bytes(0x71, 0x23, 0x0F, 0xA3) if self.device_type < 4 else self.Send_Bytes(0xCC, 0x23, 0x33)

   def Off(self):
      #Turns a device off
      self.Send_Bytes(device_ip, 0x71, 0x24, 0x0F, 0xA4) if self.device_type < 4 else self.Send_Bytes(0xCC, 0x24, 0x33)

   def Status(self):
      # Gets the current status of a device
      data = s.recv(14)
      self.Send_Bytes(device_ip, 0x81, 0x8A, 0x8B, 0x96)

   def Update_Device(self, r, g, b, white1, white2):
      # Updates a device based upon what we're sending to it
      if self.device_type <= 1:
         # Update an RGB or an RGB + WW device
         message = [0x31, r, g, b, white1, 0x00, 0x0f]
         self.Send_Bytes(*(message+[self.Calculate_Checksum(message)]))
      elif self.device_type == 2:
         # Update an RGB + WW + CW device
         message = [0x31, r, g, b, white1, white2, 0x0f, 0x0f]
         self.Send_Bytes(*(message+[self.Calculate_Checksum(message)]))
      elif self.device_type == 3:
         # Update the white, or color, of a bulb
         if white1 != None:
            message = [0x31, 0x00, 0x00, 0x00, white1, 0x0f, 0x0f]
            self.Send_Bytes(*(message+[self.Calculate_Checksum(message)]))
         else:
            message = [0x31, r, g, b, 0x00, 0xf0, 0x0f]
            self.Send_Bytes(*(message+[self.Calculate_Checksum(message)]))
      elif self.device_type == 4:
         # Update the white, or color, of a legacy bulb
         if white1 != None:
            message = [0x56, 0x00, 0x00, 0x00, w, 0x0f, 0xaa]
            self.Send_Bytes(*(message+[self.Calculate_Checksum(message)]))
         else:
            message = [0x56, r, g, b, 0x00, 0xf0, 0xaa]
            self.Send_Bytes(*(message+[self.Calculate_Checksum(message)]))
      else:
         # Incompatible device received
         print "Incompatible device type received..."

   def Send_Preset_Function(self, preset_number, speed):
      # Sends a preset command to a device
      if type <= 4:
         data = [0xBB, preset_number, speed, 0x44]
         send_bytes_action(data)
      else:
         data = [0x61, preset_number, speed, 0x0F]
         send_bytes_action(data, calc_checksum(data))

   def Calculate_Checksum(self, bytes):
      return sum(bytes) & 0xFF

   def Send_Bytes(self, *bytes):
      self.s.connect((self.device_ip, self.API_PORT))
      message_length = len(bytes)
      self.s.send(struct.pack("B"*message_length, *bytes))
      self.s.close

x = Api("10.0.1.166", 4)
x.Update_Device(255,255,255,None,None)
