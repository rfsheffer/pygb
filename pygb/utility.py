"""
GameBoy Emulator Written in Python

MIT License

Copyright (c) 2017 Ryan Sheffer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import struct


def get_size_to_pretty(the_size, in_bits=False):
    """
    Get a pretty string of a number of bits or bytes
    :param the_size: The Size in bits or bytes
    :param in_bits: Should the pretty string show bits?
    :return: A pretty string, reduced version of the_size
    """
    if the_size >= 1000000:
        return '%d%s' % (the_size / 1000000, 'MBit' if in_bits else 'MByte')
    elif the_size >= 1000:
        return '%d%s' % (the_size / 1000, 'KBit' if in_bits else 'KByte')
    return '%d%s' % (the_size, 'Bits' if in_bits else 'Bytes')


class RomInfo:
    """
    Rom Information,
    """

    # A bank is 16kb wide, so just divide the rom size kb by 16kb to get the number of banks
    rom_sizes_bits_banks = {
        0x00: (256000, 2),
        0x01: (512000, 4),
        0x02: (1000000, 8),
        0x03: (2000000, 16),
        0x04: (4000000, 32),
        0x05: (8000000, 64),
        0x06: (16000000, 128),
        0x52: (9000000, 72),
        0x53: (10000000, 80),
        0x54: (12000000, 96),
    }

    # ram banks are 8kb wide, so just divide the ram size kb by 8kb to get the number of banks
    # Note that some of the size indicies represent less than a total bank size, hence the two 1 bank entries.
    ram_sizes_bits_banks = {
        0x00: (0, 0),
        0x01: (16000, 1),
        0x02: (64000, 1),
        0x03: (256000, 4),
        0x04: (1000000, 16)
    }

    def __init__(self):
        self.rom_name = 'None'
        self.is_color = False
        self.license = 'None'
        self.super_gb = False
        self.cart_type = 0
        self.rom_size = 0
        self.ram_size = 0
        self.destination_code = 0
        self.licensee_code = ''
        self.mask_rom_ver = 0
        self.complement_check = 0
        self.checksum = 0

    def print(self):
        print('\n--------------------------------------------------------------------')
        print('Title: %s' % self.rom_name)
        print('Color: %s' % ('color' if self.is_color else 'B&W'))
        print('License: %s' % self.license)
        print('HW Type: %s' % ('Super GB' if self.super_gb else 'Normal'))
        from pygb.memory.memory import rom_memory_bank_types
        print('Cartridge Type: %s' % rom_memory_bank_types[self.cart_type])
        print('Rom Size: %s' % (self.get_size_desc(self.rom_size, self.rom_sizes_bits_banks[self.rom_size])))
        print('Ram Size: %s' % (self.get_size_desc(self.ram_size, self.ram_sizes_bits_banks[self.ram_size])))
        print('Destination Code: %s' % ('Japanese' if self.destination_code == 0 else 'Non-Japanese'))
        print('Mask Rom Version: %X' % self.mask_rom_ver)
        print('Complement Check: %d' % self.complement_check)
        print('Checksum: %d' % self.checksum)
        print('--------------------------------------------------------------------\n')

    @staticmethod
    def get_size_desc(index, num_bits_banks):
        if num_bits_banks[0] == 0:
            return 'None\t'
        num_bytes = num_bits_banks[0] / 8
        return '%d - %s =\t%s =\t%d banks' % \
               (index, get_size_to_pretty(num_bits_banks[0], True), get_size_to_pretty(num_bytes, False), num_bits_banks[1])

    def get_rom_info(self, rom_bytes):
        # Rom Name
        self.rom_name = rom_bytes[0x0134:0x0142 + 1].decode()
        # Is Color GB?
        self.is_color = rom_bytes[0x0143] == 0x80
        # Licensee Code (new): This id is only set if 0x014B doesn't contain the code
        new_licensee_code = struct.unpack_from('H', rom_bytes, 0x0144)[0]
        # Is Super GB?
        self.super_gb = rom_bytes[0x0146] == 0x03
        # Cartridge Type
        self.cart_type = rom_bytes[0x0147]
        # Rom Size
        self.rom_size = rom_bytes[0x0148]
        # Ram Size
        self.ram_size = rom_bytes[0x0149]
        # Destination Code
        self.destination_code = rom_bytes[0x014A]
        # Licensee code (old):
        self.licensee_code = rom_bytes[0x014B]
        # Determine license ID
        if self.licensee_code == 0x33:
            self.license = ("%d" % new_licensee_code)
        elif self.licensee_code == 0x79:
            self.license = 'Accolade'
        elif self.licensee_code == 0xA4:
            self.license = 'Konami'
        elif self.licensee_code == 0x01:
            self.license = 'Nintendo'
        else:
            self.license = ("%d" % self.licensee_code)
        # Mask Rom Version Number
        self.mask_rom_ver = rom_bytes[0x014C]
        # Compliment Check
        self.complement_check = 0
        # Checksum
        self.checksum = struct.unpack_from('H', rom_bytes, 0x014E)[0]
