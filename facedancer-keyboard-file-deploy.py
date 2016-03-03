#!/usr/bin/env python3

# Map char codes to usb key codes according to:
# http://www.usb.org/developers/hidpage/Hut1_12v2.pdf

codes_mapping = {}

KEY_DEFAULT_MASK = 0
KEY_CTRL_MASK    = 1
KEY_SHIFT_MASK   = 2
KEY_ALT_MASK     = 4

# Lower letters.
for code in range(ord('a'), ord('z') + 1):
    char = code
    codes_mapping[code] = bytes((KEY_DEFAULT_MASK, 0, char - ord('a') + 4))

# Upper letters.
for code in range(ord('A'), ord('Z') + 1):
    char = ord(chr(code).lower())
    codes_mapping[code] = bytes((KEY_SHIFT_MASK, 0, char - ord('a') + 4))

codes_mapping[ord('0')] = bytes((KEY_DEFAULT_MASK, 0, 0x27))
codes_mapping[ord('1')] = bytes((KEY_DEFAULT_MASK, 0, 0x1e))
codes_mapping[ord('2')] = bytes((KEY_DEFAULT_MASK, 0, 0x1f))
codes_mapping[ord('3')] = bytes((KEY_DEFAULT_MASK, 0, 0x20))
codes_mapping[ord('4')] = bytes((KEY_DEFAULT_MASK, 0, 0x21))
codes_mapping[ord('5')] = bytes((KEY_DEFAULT_MASK, 0, 0x22))
codes_mapping[ord('6')] = bytes((KEY_DEFAULT_MASK, 0, 0x23))
codes_mapping[ord('7')] = bytes((KEY_DEFAULT_MASK, 0, 0x24))
codes_mapping[ord('8')] = bytes((KEY_DEFAULT_MASK, 0, 0x25))
codes_mapping[ord('9')] = bytes((KEY_DEFAULT_MASK, 0, 0x26))

codes_mapping[ord(')')] = bytes((KEY_SHIFT_MASK, 0, 0x27))
codes_mapping[ord('!')] = bytes((KEY_SHIFT_MASK, 0, 0x1e))
codes_mapping[ord('@')] = bytes((KEY_SHIFT_MASK, 0, 0x1f))
codes_mapping[ord('#')] = bytes((KEY_SHIFT_MASK, 0, 0x20))
codes_mapping[ord('$')] = bytes((KEY_SHIFT_MASK, 0, 0x21))
codes_mapping[ord('%')] = bytes((KEY_SHIFT_MASK, 0, 0x22))
codes_mapping[ord('^')] = bytes((KEY_SHIFT_MASK, 0, 0x23))
codes_mapping[ord('&')] = bytes((KEY_SHIFT_MASK, 0, 0x24))
codes_mapping[ord('*')] = bytes((KEY_SHIFT_MASK, 0, 0x25))
codes_mapping[ord('(')] = bytes((KEY_SHIFT_MASK, 0, 0x26))

codes_mapping[ord('\n')] = bytes((KEY_DEFAULT_MASK, 0, 0x28))

codes_mapping[ord('\t')] = bytes((KEY_DEFAULT_MASK, 0, 0x2b))
codes_mapping[ord(' ')] = bytes((KEY_DEFAULT_MASK, 0, 0x2c))

codes_mapping[ord('-')] = bytes((KEY_DEFAULT_MASK, 0, 0x2d))
codes_mapping[ord('_')] = bytes((KEY_SHIFT_MASK, 0, 0x2d))

codes_mapping[ord('=')] = bytes((KEY_DEFAULT_MASK, 0, 0x2e))
codes_mapping[ord('+')] = bytes((KEY_SHIFT_MASK, 0, 0x2e))

codes_mapping[ord('[')] = bytes((KEY_DEFAULT_MASK, 0, 0x2f))
codes_mapping[ord('{')] = bytes((KEY_SHIFT_MASK, 0, 0x2f))

codes_mapping[ord(']')] = bytes((KEY_DEFAULT_MASK, 0, 0x30))
codes_mapping[ord('}')] = bytes((KEY_SHIFT_MASK, 0, 0x30))

codes_mapping[ord('\\')] = bytes((KEY_DEFAULT_MASK, 0, 0x31))
codes_mapping[ord('|')] = bytes((KEY_SHIFT_MASK, 0, 0x31))

codes_mapping[ord(';')] = bytes((KEY_DEFAULT_MASK, 0, 0x33))
codes_mapping[ord(':')] = bytes((KEY_SHIFT_MASK, 0, 0x33))

codes_mapping[ord('\'')] = bytes((KEY_DEFAULT_MASK, 0, 0x34))
codes_mapping[ord('"')] = bytes((KEY_SHIFT_MASK, 0, 0x34))

codes_mapping[ord('`')] = bytes((KEY_DEFAULT_MASK, 0, 0x35))
codes_mapping[ord('~')] = bytes((KEY_SHIFT_MASK, 0, 0x35))

codes_mapping[ord(',')] = bytes((KEY_DEFAULT_MASK, 0, 0x36))
codes_mapping[ord('<')] = bytes((KEY_SHIFT_MASK, 0, 0x36))

codes_mapping[ord('.')] = bytes((KEY_DEFAULT_MASK, 0, 0x37))
codes_mapping[ord('>')] = bytes((KEY_SHIFT_MASK, 0, 0x37))

codes_mapping[ord('.')] = bytes((KEY_DEFAULT_MASK, 0, 0x37))
codes_mapping[ord('>')] = bytes((KEY_SHIFT_MASK, 0, 0x37))

codes_mapping[ord('/')] = bytes((KEY_DEFAULT_MASK, 0, 0x38))
codes_mapping[ord('?')] = bytes((KEY_SHIFT_MASK, 0, 0x38))

# Define USB interface and device.

import sys

if len(sys.argv) != 2:
    print('Usage: {} <file>'.format(sys.argv[0]))
    exit(0)

from USB import *
from USBDevice import *
from USBConfiguration import *
from USBInterface import *
from USBEndpoint import *

class USBKeyboardInterface(USBInterface):
    name = "USB keyboard interface"

    hid_descriptor = b'\x09\x21\x10\x01\x00\x01\x22\x2b\x00'
    report_descriptor = b'\x05\x01\x09\x06\xA1\x01\x05\x07\x19\xE0\x29\xE7\x15\x00\x25\x01\x75\x01\x95\x08\x81\x02\x95\x01\x75\x08\x81\x01\x19\x00\x29\x65\x15\x00\x25\x65\x75\x08\x95\x01\x81\x00\xC0'

    def __init__(self, verbose=0):
        descriptors = { 
                USB.desc_type_hid    : self.hid_descriptor,
                USB.desc_type_report : self.report_descriptor
        }

        self.endpoint = USBEndpoint(
                3,                                      # endpoint number
                USBEndpoint.direction_in,
                USBEndpoint.transfer_type_interrupt,
                USBEndpoint.sync_type_none,
                USBEndpoint.usage_type_data,
                16384,                                  # max packet size
                1,                                      # polling interval
                self.handle_buffer_available            # handler function
        )

        USBInterface.__init__(
                self,
                0,          # interface number
                0,          # alternate setting
                3,          # interface class
                0,          # subclass
                0,          # protocol
                0,          # string index
                verbose,
                [ self.endpoint ],
                descriptors
        )

        self.keys = []

        self.append_delay(100)

        self.keys.append(bytes((KEY_CTRL_MASK | KEY_ALT_MASK, 0, ord('t') - ord('a') + 4))) # <CTRL-ALT-T>
        self.keys.append(bytes((KEY_DEFAULT_MASK, 0, 0x00))) # <KEY UP>

        self.append_delay(100)

        with open(sys.argv[1]) as f:
            self.append_save_file(sys.argv[1], f.read())

    def append_delay(self, length):
        for i in range(length):
            self.keys.append(bytes((KEY_DEFAULT_MASK, 0, 0x00)))

    def append_string(self, s):
        for c in s:
            self.keys.append(codes_mapping[ord(c)])                 # <KEY DOWN>
            self.keys.append(bytes((KEY_DEFAULT_MASK, 0, 0x00)))    # <KEY UP>

    def append_save_file(self, name, text):
        self.append_string('cat > {} << EOL\n'.format(name))
        self.append_string(text)
        self.append_string('EOL\n')

    def handle_buffer_available(self):
        if len(self.keys) == 0:
            return

        data = self.keys.pop(0)
        self.endpoint.send(data)

class USBKeyboardDevice(USBDevice):
    name = "USB keyboard device"

    def __init__(self, maxusb_app, verbose=0):
        config = USBConfiguration(
                1,                              # index
                "Emulated Keyboard",            # string desc
                [ USBKeyboardInterface() ]      # interfaces
        )

        USBDevice.__init__(
                self,
                maxusb_app,
                0,                      # device class
                0,                      # device subclass
                0,                      # protocol release number
                64,                     # max packet size for endpoint 0
                0x610b,                 # vendor id
                0x4653,                 # product id
                0x3412,                 # device revision
                "Maxim",                # manufacturer string
                "MAX3420E Enum Code",   # product string
                "S/N3420E",             # serial number string
                [ config ],
                verbose=verbose
        )

# Run. Press CTRL+C to exit.

from Facedancer import *
from MAXUSBApp import *

sp = GoodFETSerialPort()
fd = Facedancer(sp, verbose=1)
u = MAXUSBApp(fd, verbose=1)

d = USBKeyboardDevice(u, verbose=4)

d.connect()

try:
    d.run()
except KeyboardInterrupt:
    d.disconnect()
