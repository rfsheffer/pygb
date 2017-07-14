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

import os
import argparse

from pygb.cpu.cpu import CPU
from pygb.memory.memory import MemoryPool
from pygb.utility import RomInfo

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--rom', dest='rom', action='store', default='',
                    help='The rom to load')
args = parser.parse_args()


def main():
    """
    Execute the software, begin Rom selection, begin CPU
    """
    if len(args.rom) > 0 and os.path.isfile(args.rom):
        f = open(args.rom, 'rb')
        rom_bytes = f.read()
        f.close()

        # Parse the rom header and get all necessary information so we can setup our environment
        rom_info = RomInfo()
        rom_info.get_rom_info(rom_bytes)
        rom_info.print()

        # Create a memory space based on the requirements of the rom
        mem_space = MemoryPool()

        # Load in the Rom
        mem_space.load_rom(rom_bytes, rom_info.cart_type)

        # Read in the initial program
        print("Running Program...")
        cpu = CPU(mem_space)
        cpu.reset()
        while True:
            cpu.step()


if __name__ == '__main__':
    main()
