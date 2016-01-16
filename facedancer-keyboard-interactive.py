#!/usr/bin/env python3

# Interactive facedancer keyboard.

# Replace the print builtin to not let curses mess up goodfet logs.

class PrintWrapper:
    def __init__(self):
        self.saved = []
        self.original = __builtins__.__dict__['print']
        self.fake = lambda *args: self.saved.append(args)

    def fake_print(self):
        __builtins__.__dict__['print'] = self.fake

    def restore_print(self):
        __builtins__.__dict__['print'] = self.original

    def dump(self):
        for args in self.saved:
            self.original(*args)
        self.saved = []

print_wrapper = PrintWrapper()
print_wrapper.fake_print()

# Map curses key codes to usb key codes according to:
# http://www.usb.org/developers/hidpage/Hut1_12v2.pdf

import curses

codes_mapping = {}

KEY_DEFAULT_MASK = 0
KEY_CTRL_MASK    = 1
KEY_SHIFT_MASK   = 2
KEY_ALT_MASK     = 4

# <KEY>
for code in range(ord('a'), ord('z') + 1):
    char = code
    codes_mapping[code] = bytes((KEY_DEFAULT_MASK, 0, char - ord('a') + 4))

# <CTRL + KEY>
for code in range(1, 26 + 1):
    char = code - 1 + ord('a')
    codes_mapping[code] = bytes((KEY_CTRL_MASK, 0, char - ord('a') + 4))

# <SHIFT + KEY>
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

codes_mapping[ord('\n')] = bytes((KEY_DEFAULT_MASK, 0, 0x28))              # <ENTER>
codes_mapping[0x1b] = bytes((KEY_DEFAULT_MASK, 0, 0x29))                   # <ESCAPE>

codes_mapping[curses.KEY_BACKSPACE] = bytes((KEY_DEFAULT_MASK, 0, 0x2a))   # <BACKSPACE>

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

codes_mapping[curses.KEY_DC] = bytes((KEY_DEFAULT_MASK, 0, 0x4c))          # <DELETE>

codes_mapping[curses.KEY_RIGHT] = bytes((KEY_DEFAULT_MASK, 0, 0x4f))
codes_mapping[curses.KEY_LEFT] = bytes((KEY_DEFAULT_MASK, 0, 0x50))
codes_mapping[curses.KEY_DOWN] = bytes((KEY_DEFAULT_MASK, 0, 0x51))
codes_mapping[curses.KEY_UP] = bytes((KEY_DEFAULT_MASK, 0, 0x52))

# Define USB interface and device.

from USB import *
from USBDevice import *
from USBConfiguration import *
from USBInterface import *
from USBEndpoint import *

class USBKeyboardInterface(USBInterface):
    name = "USB keyboard interface"

    hid_descriptor = b'\x09\x21\x10\x01\x00\x01\x22\x2b\x00'
    report_descriptor = b'\x05\x01\x09\x06\xA1\x01\x05\x07\x19\xE0\x29\xE7\x15\x00\x25\x01\x75\x01\x95\x08\x81\x02\x95\x01\x75\x08\x81\x01\x19\x00\x29\x65\x15\x00\x25\x65\x75\x08\x95\x01\x81\x00\xC0'

    def __init__(self, screen, verbose=0):
        descriptors = { 
                USB.desc_type_hid    : self.hid_descriptor,
                USB.desc_type_report : self.report_descriptor
        }

        self.endpoint = USBEndpoint(
                3,          # endpoint number
                USBEndpoint.direction_in,
                USBEndpoint.transfer_type_interrupt,
                USBEndpoint.sync_type_none,
                USBEndpoint.usage_type_data,
                16384,      # max packet size
                10,         # polling interval, see USB 2.0 spec Table 9-13
                self.handle_buffer_available    # handler function
        )

        # TODO: un-hardcode string index (last arg before "verbose")
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

        self.screen = screen
        self.keys = []

    def handle_buffer_available(self):
        while True:
            code = self.screen.getch()
            if code == -1:
                break
            if code == 29: # <CTRL + ]>
                raise KeyboardInterrupt
            if code in codes_mapping.keys():
                self.keys.append(codes_mapping[code])                   # <KEY DOWN>
                self.keys.append(bytes((KEY_DEFAULT_MASK, 0, 0x00)))    # <KEY UP>
            break

        if len(self.keys) == 0:
            return

        data = self.keys.pop(0)

        if self.verbose > 2:
            print(self.name, "sending keypress 0x%02x" % ord(code))

        self.endpoint.send(data)

class USBKeyboardDevice(USBDevice):
    name = "USB keyboard device"

    def __init__(self, maxusb_app, screen, verbose=0):
        config = USBConfiguration(
                1,                                          # index
                "Emulated Keyboard",                        # string desc
                [ USBKeyboardInterface(screen) ]            # interfaces
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

# Run. Press CTRL+] to exit.

from Facedancer import *
from MAXUSBApp import *

try:
    screen = curses.initscr()
    screen.nodelay(1)
    screen.keypad(1)

    curses.raw()

    sp = GoodFETSerialPort()
    fd = Facedancer(sp, verbose=1)
    u = MAXUSBApp(fd, verbose=1)

    d = USBKeyboardDevice(u, screen, verbose=4)

    d.connect()

    try:
        d.run()
    except KeyboardInterrupt:
        d.disconnect()
finally:
    curses.endwin()
    print_wrapper.restore_print()
    print_wrapper.dump()
