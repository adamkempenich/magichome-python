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

import socket
import csv

class Api:
   API_PORT = 5577
   
   def On(type):
      #Turns a device on
      Send_Bytes(0x71, 0x23, 0x0F, 0xA3) if type <= 4 else Send_Bytes(0xCC, 0x23, 0x33)

   def Off(type):
      #Turns a device off
      Send_Bytes(0x71, 0x24, 0x0F, 0xA4) if type <= 4 else Send_Bytes(0xCC, 0x24, 0x33)

   def Status(type):
      # Gets the current status of a device
      data = s.recv(14)
      Send_Bytes(0x81, 0x8A, 0x8B, 0x96)

   def Update_Device(type, r, g, b, white1, white2):
      # Updates a device based upon what we're sending to it
      if type <= 1:
         # Update an RGB or an RGB + WW device
         message = [0x31, r, g, b, white1, 0x00, 0x0f]
         Send_Bytes(*message, Calculate_Checksum(message))
      elif type = 2:
         # Update an RGB + WW + CW device
         message = [0x31, r, g, b, white1, white2, 0x0f, 0x0f]
         Send_Bytes(*message, Calculate_Checksum(message))
      elif type = 3:
         # Update the white, or color, of a bulb
         if white1 != 'null':
            message = [0x31, 0x00, 0x00, 0x00, white1, 0x0f, 0x0f]
            Send_Bytes(*message, Calculate_Checksum(message))
         else:
            message = [0x31, r, g, b, 0x00, 0xf0, 0x0f]
            Send_Bytes(*message, Calculate_Checksum(message))
      elif type = 4:
         # Update the white, or color, of a legacy bulb
         if white1 != 'null':
            message = [0x56, 0x00, 0x00, 0x00, w, 0x0f, 0xaa]
            Send_Bytes(*message, Calculate_Checksum(message))
         else:
            message = [0x56, r, g, b, 0x00, 0xf0, 0xaa]
            Send_Bytes(*message, Calculate_Checksum(message))
      else:
         # Incompatible device received
         print "Incompatible device type received..."

   def Send_Preset_Function(type, preset_number, speed):
      # Sends a preset command to a device
      if type <= 4:
         data = [0xBB, preset_number, speed, 0x44]
         send_bytes_action(*data)
      else:
         data = [0x61, preset_number, speed, 0x0F]
         send_bytes_action(*data, calc_checksum(data))

   def Calculate_Checksum(bytes):
      return bytes.reduce(:+) % 0x100

   def Send_Bytes(*bytes):
      s.send(struct.pack(c, bytes))

   def Send_Bytes_Action(*bytes):
      Socket_Action { Send_Bytes(*bytes) }

   def Create_Socket(ip):
      s.close if s is !None
      global s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.connect((ip, TCP_PORT))

      s.send(MESSAGE)
      
      s.close()


   def Socket_Action:









