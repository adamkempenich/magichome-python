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

import socket, csv, struct, datetime

class MagicHome_Wifi_Api:   
   def __init__(self, device_ip, device_type, keep_alive=True):
      self.device_ip = device_ip
      self.device_type = device_type
      self.API_PORT = 5577
      self.latest_connection = datetime.datetime.now()
      self.keep_alive = keep_alive
      self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.s.settimeout(3)
      try:
         print "Establishing connection with the device."
         self.s.connect((self.device_ip, self.API_PORT))
      except socket.error, exc:
         print "Caught exception socket.error : %s" % exc
         if self.s: 
             self.s.close() 
         

   def On(self):
      #Turns a device on
      self.Send_Bytes(0x71, 0x23, 0x0F, 0xA3) if self.device_type < 4 else self.Send_Bytes(0xCC, 0x23, 0x33)

   def Off(self):
      #Turns a device off
      self.Send_Bytes(0x71, 0x24, 0x0F, 0xA4) if self.device_type < 4 else self.Send_Bytes(0xCC, 0x24, 0x33)

   def Status(self):
      # Gets the current status of a device
      if self.device_type ==2:
         self.Send_Bytes(0x81, 0x8A, 0x8B, 0x96)
         return self.s.recv(15)
      else:
         self.Send_Bytes(0x81, 0x8A, 0x8B, 0x96)
         return self.s.recv(14)
         
   def Update_Device(self, r=0, g=0, b=0, white1=None, white2=None):
      # Updates a device based upon what we're sending to it
      # Values are excepted as integers between 0-255.
      # Whites can have a value of None.

      if self.device_type <= 1:
         # Update an RGB or an RGB + WW device
         white1 = self.Check_Number_Range(white1)
         message = [0x31, r, g, b, white1, 0x00, 0x0f]
         self.Send_Bytes(*(message+[self.Calculate_Checksum(message)]))

      elif self.device_type == 2:
         # Update an RGB + WW + CW device
         message = [0x31, self.Check_Number_Range(r), self.Check_Number_Range(g), self.Check_Number_Range(b), self.Check_Number_Range(white1), self.Check_Number_Range(white2), 0x0f, 0x0f]
         self.Send_Bytes(*(message+[self.Calculate_Checksum(message)]))

      elif self.device_type == 3:
         # Update the white, or color, of a bulb
         if white1 != None:
            message = [0x31, 0x00, 0x00, 0x00, self.Check_Number_Range(white1), 0x0f, 0x0f]
            self.Send_Bytes(*(message+[self.Calculate_Checksum(message)]))
         else:
            message = [0x31, self.Check_Number_Range(r), self.Check_Number_Range(g), self.Check_Number_Range(b), 0x00, 0xf0, 0x0f]
            self.Send_Bytes(*(message+[self.Calculate_Checksum(message)]))

      elif self.device_type == 4:
         # Update the white, or color, of a legacy bulb
         if white1 != None:
            message = [0x56, 0x00, 0x00, 0x00, self.Check_Number_Range(white1), 0x0f, 0xaa, 0x56, 0x00, 0x00, 0x00, self.Check_Number_Range(white1), 0x0f, 0xaa]
            self.Send_Bytes(*(message+[self.Calculate_Checksum(message)]))
         else:
            message = [0x56, self.Check_Number_Range(r), self.Check_Number_Range(g), self.Check_Number_Range(b), 0x00, 0xf0, 0xaa]
            self.Send_Bytes(*(message+[self.Calculate_Checksum(message)]))
      else:
         # Incompatible device received
         print "Incompatible device type received..."

   def Check_Number_Range(self, number):
      if number < 0:
         return 0 
      elif number > 255:
         return 255
      else:
         return number

   def Send_Preset_Function(self, preset_number, speed):
      # Sends a preset command to a device
      # Presets can range from 0x25 (int 37) to 0x38 (int 56)
      if preset_number < 37:
         preset_number = 37
      if preset_number > 56:
         preset_number = 56
      if speed < 0:
         speed = 0
      if speed > 100:
         speed = 100

      if type == 4:
         self.Send_Bytes(0xBB, preset_number, speed, 0x44)
      else:
         message = [0x61, preset_number, speed, 0x0F]
         self.Send_Bytes(*(message+[self.Calculate_Checksum(message)]))

   def Calculate_Checksum(self, bytes):
      # Calculates the checksum from an array of bytes
      return sum(bytes) & 0xFF

   def Send_Bytes(self, *bytes):
      # Sends commands to the device
      # If the device hasn't been communicated to in 5 minutes, reestablish the connection
      check_connection_time = (datetime.datetime.now()-self.latest_connection).total_seconds()
      try:
         if check_connection_time >= 290:
            print "Connection timed out, reestablishing."
            self.s.connect((self.device_ip, self.API_PORT))
         message_length = len(bytes)
         self.s.send(struct.pack("B"*message_length, *bytes))
         # Close the connection unless requested not to 
         if self.keep_alive == False:
            self.s.close
      except socket.error, exc:
         print "Caught exception socket.error : %s" % exc
         if self.s: 
             self.s.close() 
