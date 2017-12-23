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


class Interrupts(object):
    INTERRUPT_VBLANK = 0x01
    INTERRUPT_LCDSTAT = 0x02
    INTERRUPT_TIMER = 0x04
    INTERRUPT_SERIAL = 0x08
    INTERRUPT_JOYPAD = 0x10

    # Addresses in memory for interrupt settings
    INTERRUPT_ENABLE_ADDR = 0xFFFF
    INTERRUPT_FLAG_ADDR = 0xFF0F

    def __init__(self):
        # Interrupt Master Enable
        # This controls whether the interrupt routines are enabled.
        # Disabling this via the DI instruction will halt all interrupt activity.
        self.IME = 0x1

    def step(self, memory):
        """
        Steps the interrupt sub routines
        :param memory: The memory Pool for the system
        """

        if not self.IME:
            return

        # Get from memory the current enable flag
        interrupt_enabled = memory.read_byte(self.INTERRUPT_ENABLE_ADDR)

        # Get from memory the current interrupt sub routine to run
        interrupt_flag = memory.read_byte(self.INTERRUPT_FLAG_ADDR)

        active_interrupts = interrupt_enabled & interrupt_flag

        # Run through all the interrupts, running them if necessary
        if active_interrupts & self.INTERRUPT_VBLANK:
            memory.write_byte(self.INTERRUPT_FLAG_ADDR, interrupt_flag & ~self.INTERRUPT_VBLANK)
            self.vblank()

        if active_interrupts & self.INTERRUPT_LCDSTAT:
            memory.write_byte(self.INTERRUPT_FLAG_ADDR, interrupt_flag & ~self.INTERRUPT_LCDSTAT)
            self.lcd_stat()

        if active_interrupts & self.INTERRUPT_TIMER:
            memory.write_byte(self.INTERRUPT_FLAG_ADDR, interrupt_flag & ~self.INTERRUPT_TIMER)
            self.timer()

        if active_interrupts & self.INTERRUPT_SERIAL:
            memory.write_byte(self.INTERRUPT_FLAG_ADDR, interrupt_flag & ~self.INTERRUPT_SERIAL)
            self.serial()

        if active_interrupts & self.INTERRUPT_JOYPAD:
            memory.write_byte(self.INTERRUPT_FLAG_ADDR, interrupt_flag & ~self.INTERRUPT_JOYPAD)
            self.joypad()

    def vblank(self):
        """
        The V-Blank interrupt occurs ~59.7 times a second
        on a regular GB and ~61.1 times a second on a Super
        GB (SGB). This interrupt occurs at the beginning of
        the V-Blank period. During this period video
        hardware is not using video ram so it may be freely
        accessed. This period lasts approximately 1.1 ms.
        """
        pass

    def lcd_stat(self):
        """
        There are various reasons for this interrupt to
        occur as described by the STAT register ($FF40). One
        very popular reason is to indicate to the user when
        the video hardware is about to redraw a given LCD
        line. This can be useful for dynamically controlling
        the SCX/SCY registers ($FF43/$FF42) to perform
        special video effects.
        """
        pass

    def timer(self):
        """
        This interrupt occurs when the TIMA register ($FF05)
        changes from $FF to $00.
        """
        pass

    def serial(self):
        """
        This interrupt occurs when a serial transfer has
        completed on the game link port.
        """
        pass

    def joypad(self):
        pass
