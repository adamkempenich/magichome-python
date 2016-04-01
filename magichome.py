"""MagicHome Python API.

Copyright 2016, Adam Kempenich. Licensed under MIT.

It currently supports:
- Bulbs (Firmware v.4 and greater)
- Legacy Bulbs (Firmware v.3 and lower)
- RGB Controllers
- RGB+WW Controllers
- RGB+WW+CW Controllers
"""
import socket
import csv
import struct
import datetime


class MagicHomeApi:
    """Representation of a MagicHome device."""

    def __init__(self, device_ip, device_type, keep_alive=True):
        """"Initialize a device."""
        self.device_ip = device_ip
        self.device_type = device_type
        self.API_PORT = 5577
        self.latest_connection = datetime.datetime.now()
        self.keep_alive = keep_alive
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(3)
        try:
            print("Establishing connection with the device.")
            self.s.connect((self.device_ip, self.API_PORT))
        except socket.error as exc:
            print("Caught exception socket.error : %s" % exc)
            if self.s:
                self.s.close()

    def turn_on(self):
        """Turn a device on."""
        self.send_bytes(0x71, 0x23, 0x0F, 0xA3) if self.device_type < 4 else self.send_bytes(0xCC, 0x23, 0x33)

    def turn_off(self):
        """Turn a device off."""
        self.send_bytes(0x71, 0x24, 0x0F, 0xA4) if self.device_type < 4 else self.send_bytes(0xCC, 0x24, 0x33)

    def get_status(self):
        """Get the current status of a device."""
        if self.device_type == 2:
            self.send_bytes(0x81, 0x8A, 0x8B, 0x96)
            return self.s.recv(15)
        else:
            self.send_bytes(0x81, 0x8A, 0x8B, 0x96)
            return self.s.recv(14)

    def update_device(self, r=0, g=0, b=0, white1=None, white2=None):
        """Updates a device based upon what we're sending to it.

        Values are excepted as integers between 0-255.
        Whites can have a value of None.
        """
        if self.device_type <= 1:
            # Update an RGB or an RGB + WW device
            white1 = self.check_number_range(white1)
            message = [0x31, r, g, b, white1, 0x00, 0x0f]
            self.send_bytes(*(message+[self.calculate_checksum(message)]))

        elif self.device_type == 2:
            # Update an RGB + WW + CW device
            message = [0x31,
                       self.check_number_range(r),
                       self.check_number_range(g),
                       self.check_number_range(b),
                       self.check_number_range(white1),
                       self.check_number_range(white2),
                       0x0f, 0x0f]
            self.send_bytes(*(message+[self.calculate_checksum(message)]))

        elif self.device_type == 3:
            # Update the white, or color, of a bulb
            if white1 is not None:
                message = [0x31, 0x00, 0x00, 0x00,
                           self.check_number_range(white1),
                           0x0f, 0x0f]
                self.send_bytes(*(message+[self.calculate_checksum(message)]))
            else:
                message = [0x31,
                           self.check_number_range(r),
                           self.check_number_range(g),
                           self.check_number_range(b),
                           0x00, 0xf0, 0x0f]
                self.send_bytes(*(message+[self.calculate_checksum(message)]))

        elif self.device_type == 4:
            # Update the white, or color, of a legacy bulb
            if white1 != None:
                message = [0x56, 0x00, 0x00, 0x00,
                           self.check_number_range(white1),
                           0x0f, 0xaa, 0x56, 0x00, 0x00, 0x00,
                           self.check_number_range(white1),
                           0x0f, 0xaa]
                self.send_bytes(*(message+[self.calculate_checksum(message)]))
            else:
                message = [0x56,
                           self.check_number_range(r),
                           self.check_number_range(g),
                           self.check_number_range(b),
                           0x00, 0xf0, 0xaa]
                self.send_bytes(*(message+[self.calculate_checksum(message)]))
        else:
            # Incompatible device received
            print("Incompatible device type received...")

    def check_number_range(self, number):
        """Check if the given number is in the allowed range."""
        if number < 0:
            return 0
        elif number > 255:
            return 255
        else:
            return number

    def send_preset_function(self, preset_number, speed):
        """Send a preset command to a device."""
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
            self.send_bytes(0xBB, preset_number, speed, 0x44)
        else:
            message = [0x61, preset_number, speed, 0x0F]
            self.send_bytes(*(message+[self.calculate_checksum(message)]))

    def calculate_checksum(self, bytes):
        """Calculate the checksum from an array of bytes."""
        return sum(bytes) & 0xFF

    def send_bytes(self, *bytes):
        """Send commands to the device.

        If the device hasn't been communicated to in 5 minutes, reestablish the
        connection.
        """
        check_connection_time = (datetime.datetime.now() -
                                 self.latest_connection).total_seconds()
        try:
            if check_connection_time >= 290:
                print("Connection timed out, reestablishing.")
                self.s.connect((self.device_ip, self.API_PORT))
            message_length = len(bytes)
            self.s.send(struct.pack("B"*message_length, *bytes))
            # Close the connection unless requested not to
            if self.keep_alive is False:
                self.s.close
        except socket.error as exc:
            print("Caught exception socket.error : %s" % exc)
            if self.s:
                self.s.close()
