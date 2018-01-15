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

from pygb.utility import gb_type_select_var
from pygb.memory.memory import MemoryLocations, MemorySizes

class Capabilities:
    """
    The capabilities of the GameBoy video hardware
    """
    mem_size = 0x2000

    screen_width = 160
    screen_height = 144

    # Refresh rates
    horiz_sync_khz = 9198
    vert_sync_hz = 59.73

    sgb_horiz_sync_khz = 9420
    sgb_vert_sync_hz = 61.17

    # Sprites
    max_sprite_width = 8
    max_sprite_height = 16
    min_sprite_width = 8
    min_sprite_height = 8

class Video:
    # The LCD controller is in the H-Blank period and
    # the CPU can access both the display RAM (8000h-9FFFh)
    # and OAM (FE00h-FE9Fh)
    VIDEO_MODE_HBLANK = 0

    # The LCD contoller is in the V-Blank period (or the
    # display is disabled) and the CPU can access both the
    # display RAM (8000h-9FFFh) and OAM (FE00h-FE9Fh)
    VIDEO_MODE_VBLANK = 1

    # The LCD controller is reading from OAM memory.
    # The CPU <cannot> access OAM memory (FE00h-FE9Fh)
    # during this period.
    VIDEO_MODE_OAM_READ = 2

    # The LCD controller is reading from both OAM and VRAM,
    # The CPU <cannot> access OAM and VRAM during this period.
    # CGB Mode: Cannot access Palette Data (FF69,FF6B) either.
    VIDEO_MODE_OAM_VRAM_READ = 3

    # Specifies the position in the 256x256 pixels BG map (32x32 tiles) which is to be displayed at the upper/left
    # LCD display position. Values in range from 0-255 may be used for X/Y each, the video controller automatically
    # wraps back to the upper (left) position in BG map when drawing exceeds the lower (right) border of the BG map
    # area.
    SCY_ADDR = 0xFF42 # Scroll Y (R/W)
    SCX_ADDR = 0xFF43 # Scroll X (R/W)

    # The LY indicates the vertical line to which the present data is transferred to the LCD Driver. The LY can take
    # on any value between 0 through 153. The values between 144 and 153 indicate the V-Blank period. Writing will
    # reset the counter.
    LY_ADDR = 0xFF44 # LCDC Y-Coordinate (R)

    # The gameboy permanently compares the value of the LYC and LY registers. When both values are identical, the
    # coincident bit in the STAT register becomes set, and (if enabled) a STAT interrupt is requested.
    LYC_ADDR = 0xFF45 # LY Compare (R/W)

    # Specifies the upper/left positions of the Window area. (The window is an alternate background area which can be
    # displayed above of the normal background. OBJs (sprites) may be still displayed above or behind the window,
    # just as for normal BG.) The window becomes visible (if enabled) when positions are set in range
    # WX=0..166, WY=0..143. A position of WX=7, WY=0 locates the window at upper left, it is then completely covering
    # normal background.
    WY_ADDR = 0xFF4A # Window Y Position (R/W)
    WX_ADDR = 0xFF4B # Window X Position minus 7 (R/W)

    LY_VBLANK_RANGE = list(range(144, 153))

    """
    The GameBoy Graphics Processing
    """
    def __init__(self, memory_space):
        self.memory = memory_space

        self.horiz_sync_hz = Capabilities.horiz_sync_khz * 1000
        self.vert_sync_hz = Capabilities.vert_sync_hz

        # Current Front Buffer (Pixel Presentation)
        self.front_buffer = None


        self.mode_flag = self.VIDEO_MODE_HBLANK
        self.mode_LY_counter = 0

        # Temp to get things moving along, a bad mode cycle tick
        self.oam_counter = 0

    def reset(self, gb_type):
        self.horiz_sync_hz = gb_type_select_var(gb_type,
                                                Capabilities.horiz_sync_khz * 1000,
                                                Capabilities.sgb_horiz_sync_khz * 1000,
                                                Capabilities.horiz_sync_khz * 1000,
                                                Capabilities.horiz_sync_khz * 1000)
        self.vert_sync_hz = gb_type_select_var(gb_type,
                                                Capabilities.vert_sync_hz,
                                                Capabilities.sgb_vert_sync_hz,
                                                Capabilities.vert_sync_hz,
                                                Capabilities.vert_sync_hz)

        self.front_buffer = bytearray(Capabilities.screen_width * Capabilities.screen_height)

        self.mode_flag = self.VIDEO_MODE_HBLANK
        self.mode_LY_counter = 0

        self.oam_counter = 0

    def step(self):
        if self.mode_flag == self.VIDEO_MODE_HBLANK:
            self.hblank()
        elif self.mode_flag == self.VIDEO_MODE_VBLANK:
            self.vblank()
        elif self.mode_flag == self.VIDEO_MODE_OAM_READ:
            self.oam_read()
        elif self.mode_flag == self.VIDEO_MODE_OAM_VRAM_READ:
            self.oam_vram_read()

    def hblank(self):
        self.mode_LY_counter += 1
        self.memory.write_byte(self.LY_ADDR, self.mode_LY_counter)

        if self.mode_LY_counter in self.LY_VBLANK_RANGE:
            self.mode_flag = self.VIDEO_MODE_VBLANK


    def vblank(self):
        self.mode_LY_counter += 1
        self.memory.write_byte(self.LY_ADDR, self.mode_LY_counter)

        if self.mode_LY_counter == self.LY_VBLANK_RANGE[len(self.LY_VBLANK_RANGE) - 1] + 1:
            self.mode_LY_counter = 0
            self.memory.write_byte(self.LY_ADDR, self.mode_LY_counter)
            self.mode_flag = self.VIDEO_MODE_OAM_READ

    def oam_read(self):
        self.oam_counter += 1
        if self.oam_counter == 200:
            self.mode_flag = self.VIDEO_MODE_OAM_VRAM_READ
            self.oam_counter = 0

    def oam_vram_read(self):
        self.oam_counter += 1
        if self.oam_counter == 200:
            self.mode_flag = self.VIDEO_MODE_HBLANK
            self.oam_counter = 0
