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

from pygb.cpu.cpu import CPU
from pygb.video.video import Video
from pygb.memory.memory import MemoryPool
from pygb.utility import RomInfo
from pygb.utility import GBTypes

class GameBoy:
    """
    The GameBoy Unit itself
    """
    def __init__(self, gb_type):
        self.game_boy_type = gb_type
        self.memory = MemoryPool()
        self.cpu = CPU(self.memory)
        self.video = Video(self.memory)
        self.sound = None

    def reset(self):
        # Always reset memory first.
        self.memory.reset(self.game_boy_type)

        self.cpu.reset(self.game_boy_type)
        self.video.reset(self.game_boy_type)

    def load_rom(self, rom_path):
        f = open(rom_path, 'rb')
        rom_bytes = f.read()
        f.close()

        # Parse the rom header and get all necessary information so we can setup our environment
        rom_info = RomInfo()
        rom_info.get_rom_info(rom_bytes)
        rom_info.print()

        if rom_info.super_gb and self.game_boy_type != GBTypes.gameboy_super:
            self.game_boy_type = GBTypes.gameboy_super
            print('Switching to Super GameBoy Mode!')

        self.reset()
        self.memory.load_rom(rom_bytes, rom_info.cart_type)

    def run_cpu(self):
        while True:
            self.cpu.step()
            self.video.step()
