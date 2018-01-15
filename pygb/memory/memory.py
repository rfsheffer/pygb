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

from copy import deepcopy
import pygb.settings
from pygb.utility import get_size_to_pretty, gb_type_select_var


class Capabilities:
    """
    The capabilities of the GameBoy main memory
    """
    pass

# Rom Memory bank types for extended rom.
# Some roms go beyond the fixed rom 32kb fixed rom space of the device.
# When this happens, a number of 16kb banks are open for use. On request
# one of these banks is mapped to the switch_rom_bank area of device memory address space.
# Capabilities are split with the + symbol
rom_memory_bank_types = {
    0x00: "ROM ONLY",
    0x01: "ROM+MBC1",
    0x02: "ROM+MBC1+RAM",
    0x03: "ROM+MBC1+RAM+BATT",
    0x05: "ROM+MBC2",
    0x06: "ROM+MBC2+BATTERY",
    0x08: "ROM+RAM",
    0x09: "ROM+RAM+BATTERY",
    0x0B: "ROM+MMM01",
    0x0C: "ROM+MMM01+SRAM",
    0x0D: "ROM+MMM01+SRAM+BATT",
    0x0F: "ROM+MBC3+TIMER+BATT",
    0x10: "ROM+MBC3+TIMER+RAM+BATT",
    0x11: "ROM+MBC3",
    0x12: "ROM+MBC3+RAM",
    0x13: "ROM+MBC3+RAM+BATT",
    0x19: "ROM+MBC5",
    0x1A: "ROM+MBC5+RAM",
    0x1B: "ROM+MBC5+RAM+BATT",
    0x1C: "ROM+MBC5+RUMBLE",
    0x1D: "ROM+MBC5+RUMBLE+SRAM",
    0x1E: "ROM+MBC5+RUMBLE+SRAM+BATT",

    # Special bank select types. Bandai and Hudson are software companies.
    # I can speculate that these two companies got early dev kits and asked
    # nintendo if their configurations could be included.
    # Pocket camera is just that creepy camera hardware with the scary error pictures.
    0x1F: "Pocket Camera",
    0xFD: "Bandai+TAMA5",
    0xFE: "Hudson+HuC-3",
    0xFF: "Hudson+HuC-1"
}


class MemorySizes:
    """
    Sizes of the individual buffers, in order
    """
    rom_bank_size = 0x4000
    switch_rom_bank_size = 0x4000

    video_ram_size = 0x2000

    switch_ram_bank_size = 0x2000

    internal_ram_size = 0x2000
    echo_internal_size = 0x1E00

    sprite_attrib_mem_size = 0xA0

    unused_io_size = 0x60

    io_ports_size = 0x4C

    unused_io_size2 = 0x34

    internal_ram_size2 = 0x7F

io_reset = [
    0x0F, 0x00, 0x7C, 0xFF, 0x00, 0x00, 0x00, 0xF8, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x01,
    0x80, 0xBF, 0xF3, 0xFF, 0xBF, 0xFF, 0x3F, 0x00, 0xFF, 0xBF, 0x7F, 0xFF, 0x9F, 0xFF, 0xBF, 0xFF,
    0xFF, 0x00, 0x00, 0xBF, 0x77, 0xF3, 0xF1, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
    0x00, 0xFF, 0x00, 0xFF, 0x00, 0xFF, 0x00, 0xFF, 0x00, 0xFF, 0x00, 0xFF, 0x00, 0xFF, 0x00, 0xFF,
    0x91, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFC, 0x00, 0x00, 0x00, 0x00, 0xFF, 0x7E, 0xFF, 0xFE,
    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x3E, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xC0, 0xFF, 0xC1, 0x00, 0xFE, 0xFF, 0xFF, 0xFF,
    0xF8, 0xFF, 0x00, 0x00, 0x00, 0x8F, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
    0xCE, 0xED, 0x66, 0x66, 0xCC, 0x0D, 0x00, 0x0B, 0x03, 0x73, 0x00, 0x83, 0x00, 0x0C, 0x00, 0x0D,
    0x00, 0x08, 0x11, 0x1F, 0x88, 0x89, 0x00, 0x0E, 0xDC, 0xCC, 0x6E, 0xE6, 0xDD, 0xDD, 0xD9, 0x99,
    0xBB, 0xBB, 0x67, 0x63, 0x6E, 0x0E, 0xEC, 0xCC, 0xDD, 0xDC, 0x99, 0x9F, 0xBB, 0xB9, 0x33, 0x3E,
    0x45, 0xEC, 0x52, 0xFA, 0x08, 0xB7, 0x07, 0x5D, 0x01, 0xFD, 0xC0, 0xFF, 0x08, 0xFC, 0x00, 0xE5,
    0x0B, 0xF8, 0xC2, 0xCE, 0xF4, 0xF9, 0x0F, 0x7F, 0x45, 0x6D, 0x3D, 0xFE, 0x46, 0x97, 0x33, 0x5E,
    0x08, 0xEF, 0xF1, 0xFF, 0x86, 0x83, 0x24, 0x74, 0x12, 0xFC, 0x00, 0x9F, 0xB4, 0xB7, 0x06, 0xD5,
    0xD0, 0x7A, 0x00, 0x9E, 0x04, 0x5F, 0x41, 0x2F, 0x1D, 0x77, 0x36, 0x75, 0x81, 0xAA, 0x70, 0x3A,
    0x98, 0xD1, 0x71, 0x02, 0x4D, 0x01, 0xC1, 0xFF, 0x0D, 0x00, 0xD3, 0x05, 0xF9, 0x00, 0x0B, 0x00
]


class MemoryLocations:
    """
    Locations of the sections in memory
    """
    rom_bank_addr = 0x0000
    switch_rom_bank_addr = rom_bank_addr + MemorySizes.rom_bank_size
    video_ram_addr = switch_rom_bank_addr + MemorySizes.switch_rom_bank_size
    switch_ram_bank_addr = video_ram_addr + MemorySizes.video_ram_size
    internal_ram_addr = switch_ram_bank_addr + MemorySizes.switch_ram_bank_size
    echo_internal_addr = internal_ram_addr + MemorySizes.internal_ram_size
    sprite_attrib_mem_addr = echo_internal_addr + MemorySizes.echo_internal_size
    unused_io_addr = sprite_attrib_mem_addr + MemorySizes.sprite_attrib_mem_size
    io_ports_addr = unused_io_addr + MemorySizes.unused_io_size
    unused_io_addr2 = io_ports_addr + MemorySizes.io_ports_size
    internal_ram_addr2 = unused_io_addr2 + MemorySizes.unused_io_size2
    interrupt_enable_addr = internal_ram_addr2 + MemorySizes.internal_ram_size2

    @staticmethod
    def print_mem_locations():
        print("ROM bank #0                : {:02X}".format(MemoryLocations.rom_bank_addr))
        print("switchable ROM bank        : {:02X}".format(MemoryLocations.switch_rom_bank_addr))
        print("Video RAM                  : {:02X}".format(MemoryLocations.video_ram_addr))
        print("switchable RAM bank        : {:02X}".format(MemoryLocations.switch_ram_bank_addr))
        print("Internal RAM               : {:02X}".format(MemoryLocations.internal_ram_addr))
        print("Echo of Internal RAM       : {:02X}".format(MemoryLocations.echo_internal_addr))
        print("Sprite Attrib Memory (OAM) : {:02X}".format(MemoryLocations.sprite_attrib_mem_addr))
        print("Empty but unusable for I/O : {:02X}".format(MemoryLocations.unused_io_addr))
        print("I/O ports                  : {:02X}".format(MemoryLocations.io_ports_addr))
        print("Empty but unusable for I/O : {:02X}".format(MemoryLocations.unused_io_addr2))
        print("Internal RAM               : {:02X}".format(MemoryLocations.internal_ram_addr2))
        print("Interrupt Enable Register  : {:02X}".format(MemoryLocations.interrupt_enable_addr))

# Debug
if pygb.settings.DEBUG:
    MemoryLocations.print_mem_locations()


class MemoryException(Exception):
    """
    Memory Pool exception
    """
    pass


class MemoryPool:
    """
    Memory Pool Object for accessing the GameBoy memory space
    """

    # Max memory address space for the GameBoy
    MAX_POOL_SIZE = 0x10000

    def __init__(self):
        # Rom Bytes
        self.rom = None

        # Rom Bytes view
        self.rv = None

        # Memory Space Bytes
        self.mem = None

        # Memory Space View
        self.mv = None

        # This will be changed if the rom is using extra, bankable memory
        self.memory_mode = 0x00  # Rom Only by default

    def load_rom(self, rom_bytes, mode_index):
        """
        Load a rom into memory. This much happen before the CPU can step.
        :param rom_bytes: The bytes of the rom
        :param mode_index: The memory bank mode type index
        """
        mode_string = rom_memory_bank_types[mode_index]
        print('Loading ROM size : {}, {}'.format(get_size_to_pretty(len(rom_bytes)), len(rom_bytes)))
        print('Rom uses bank access : {}'.format(mode_string))

        modes = mode_string.split('+')
        for mode in modes:
            if mode == 'ROM':
                # Just means we are using the ROM memory space. We can assume all software will.
                pass
            elif mode == 'MBC1':
                # 16MBit(2MByte) ROM / 8KByte RAM or 4MBit (500KByte) ROM / 32KByte RAM
                # Defaults to 16
                print('Setting up MBC1')

        # Immediately load in all rom bytes. Different memory modes address it differently.
        self.rom = bytearray(deepcopy(rom_bytes))
        self.rv = memoryview(self.rom)

        # Load bank zero into the rom bank address space, and also bank 1 into the switch space
        # In the case of a 32kb rom, switch space will stay put, so defaulting bank 1 into this space seems ideal
        self.mv[0:MemoryLocations.video_ram_addr] = self.rv[0:MemoryLocations.video_ram_addr]

    def reset(self, gb_type):
        """
        Zero all memory in the pool
        """
        if self.mv is not None:
            self.mv.release()
        self.mem = bytearray(MemoryPool.MAX_POOL_SIZE)
        self.mv = memoryview(self.mem)

        self.mem[0xFF05] = 0x00  # TIMA
        self.mem[0xFF06] = 0x00  # TMA
        self.mem[0xFF07] = 0x00  # TAC
        self.mem[0xFF10] = 0x80  # NR10
        self.mem[0xFF11] = 0xBF  # NR11
        self.mem[0xFF12] = 0xF3  # NR12
        self.mem[0xFF14] = 0xBF  # NR14
        self.mem[0xFF16] = 0x3F  # NR21
        self.mem[0xFF17] = 0x00  # NR22
        self.mem[0xFF19] = 0xBF  # NR24
        self.mem[0xFF1A] = 0x7F  # NR30
        self.mem[0xFF1B] = 0xFF  # NR31
        self.mem[0xFF1C] = 0x9F  # NR32
        self.mem[0xFF1E] = 0xBF  # NR33
        self.mem[0xFF20] = 0xFF  # NR41
        self.mem[0xFF21] = 0x00  # NR42
        self.mem[0xFF22] = 0x00  # NR43
        self.mem[0xFF23] = 0xBF  # NR30
        self.mem[0xFF24] = 0x77  # NR50
        self.mem[0xFF25] = 0xF3  # NR51
        self.mem[0xFF26] = gb_type_select_var(gb_type, 0xF1, 0xF0, 0xF1, 0xF1)  # NR52
        self.mem[0xFF40] = 0x91  # LCDC
        self.mem[0xFF42] = 0x00  # SCY
        self.mem[0xFF43] = 0x00  # SCX
        self.mem[0xFF45] = 0x00  # LYC
        self.mem[0xFF47] = 0xFC  # BGP
        self.mem[0xFF48] = 0xFF  # OBP0
        self.mem[0xFF49] = 0xFF  # OBP1
        self.mem[0xFF4A] = 0x00  # WY
        self.mem[0xFF4B] = 0x00  # WX
        self.mem[0xFFFF] = 0x00  # IE

    @staticmethod
    def check_address(address):
        """
        Check that the address is valid
        :param address: The address changed
        """
        if address < 0 or address >= MemoryPool.MAX_POOL_SIZE:
            raise MemoryException('Invalid Memory Address beyond memory address space! {:02X}'.format(address))

    def read_byte(self, address):
        """
        Read a byte from this pools memory space
        :param address: The address to read.
        :return:
        """
        if pygb.settings.DEBUG:
            self.check_address(address)
        return self.mem[address]

    def read_short(self, address, order='little'):
        if pygb.settings.DEBUG:
            self.check_address(address)
            self.check_address(address + 1)
        return int.from_bytes(self.mv[address:address + 2].tobytes(), byteorder=order)

    def write_byte(self, address, byte):
        if pygb.settings.DEBUG:
            self.check_address(address)
        self.mem[address] = byte
        self.handle_echo_space(address, byte.to_bytes(1, byteorder='big'))

    def write_short(self, address, short):
        if pygb.settings.DEBUG:
            self.check_address(address)
            self.check_address(address + 1)
        bytes_in = short.to_bytes(2, byteorder='big')
        self.mv[address:address + 2] = bytes_in
        self.handle_echo_space(address, bytes_in)

    def handle_echo_space(self, address, bytes_in):
        """
        The echo memory space "echos" the internal memory space. So any modifications to internal should update
        the echo space, and vice-versa. Note: The echo space is smaller than the internal space.
        :param address: The address to write to
        :param bytes_in: The bytes to write to the location
        """
        num_bytes = len(bytes_in)
        if MemoryLocations.echo_internal_addr <= address <= (MemoryLocations.sprite_attrib_mem_addr - num_bytes):
            # Writing to echo ram, also write to internal memory
            im_addr = MemoryLocations.internal_ram_addr + (address - MemoryLocations.echo_internal_addr)
            self.mv[im_addr:im_addr + num_bytes] = bytes_in
        else:
            max_im_addr = MemoryLocations.internal_ram_addr + \
                          (MemoryLocations.sprite_attrib_mem_addr - MemoryLocations.echo_internal_addr)
            if MemoryLocations.internal_ram_addr <= address <= (max_im_addr - num_bytes):
                # Writing to internal memory, echo change to echo address space
                im_addr = MemoryLocations.echo_internal_addr + (address - MemoryLocations.internal_ram_addr)
                self.mv[im_addr:im_addr + num_bytes] = bytes_in

    def print_memory_space(self, address, num_bytes):
        mem_space = self.mv[address:address + num_bytes]
        print(mem_space.hex())


class MemoryPoolTest:
    class MemoryPoolTestException(Exception):
        pass

    """
    GameBoy Memory Space tests
    """
    @staticmethod
    def run_test():
        MemoryPoolTest.echo_space_test()

    @staticmethod
    def echo_space_test():
        memory_pool = MemoryPool()
        memory_pool.reset(0)

        # This is the furthest address into internal ram echo can write to
        max_im_addr = MemoryLocations.internal_ram_addr + (MemoryLocations.sprite_attrib_mem_addr -
                                                           MemoryLocations.echo_internal_addr)

        # BYTE CHECK
        # Write to the start of the internal ram, except it to end up in the echo
        memory_pool.write_byte(MemoryLocations.internal_ram_addr, 0xDE)
        if memory_pool.read_byte(MemoryLocations.echo_internal_addr) != 0xDE:
            raise MemoryPoolTest.MemoryPoolTestException('Write Byte: Echo mem space start did not get written to'
                                                         ' correctly!')

        # Write to the end of the internal ram where it should be written to the echo space
        memory_pool.write_byte(max_im_addr - 1, 0xDE)
        if memory_pool.read_byte(MemoryLocations.sprite_attrib_mem_addr - 1) != 0xDE:
            raise MemoryPoolTest.MemoryPoolTestException('Write Byte: Echo mem space end did not get written to '
                                                         'correctly!')

        memory_pool.reset(0)

        # Write to the start of the echo space, expect it on internal
        memory_pool.write_byte(MemoryLocations.echo_internal_addr, 0xDE)
        if memory_pool.read_byte(MemoryLocations.internal_ram_addr) != 0xDE:
            raise MemoryPoolTest.MemoryPoolTestException('Write Byte: Internal mem space start did not get written to'
                                                         ' correctly!')

        # Write to the end of the echo space, expect it on internal
        memory_pool.write_byte(MemoryLocations.sprite_attrib_mem_addr - 1, 0xDE)
        if memory_pool.read_byte(max_im_addr - 1) != 0xDE:
            raise MemoryPoolTest.MemoryPoolTestException('Write Byte: Internal mem space end did not get written to '
                                                         'correctly!')

        memory_pool.reset(0)

        # SHORT CHECK
        # Write to the start of the internal mem, except it to end up in the echo space
        memory_pool.write_short(MemoryLocations.internal_ram_addr, 0xDEAD)
        if memory_pool.read_short(MemoryLocations.echo_internal_addr, 'big') != 0xDEAD:
            raise MemoryPoolTest.MemoryPoolTestException('Write Short: Internal mem start did not get written to '
                                                         'correctly!')

        # Write to the farthest address into the internal ram, expect the end of echo to contain the value
        memory_pool.write_short(max_im_addr - 2, 0xDEAD)
        if memory_pool.read_short(MemoryLocations.sprite_attrib_mem_addr - 2, 'big') != 0xDEAD:
            raise MemoryPoolTest.MemoryPoolTestException('Echo mem space end did not get written to correctly!')

        memory_pool.reset(0)

        # Write to the start of the echo space, expect it on internal
        memory_pool.write_short(MemoryLocations.echo_internal_addr, 0xDEAD)
        if memory_pool.read_short(MemoryLocations.internal_ram_addr, 'big') != 0xDEAD:
            raise MemoryPoolTest.MemoryPoolTestException('Write Short: Internal mem space start did not get written to'
                                                         ' correctly!')

        # Write to the end of the echo space, expect it on internal
        memory_pool.write_short(MemoryLocations.sprite_attrib_mem_addr - 2, 0xDEAD)
        if memory_pool.read_short(max_im_addr - 2, 'big') != 0xDEAD:
            raise MemoryPoolTest.MemoryPoolTestException('Write Short: Internal mem space end did not get written to '
                                                         'correctly!')

        memory_pool.reset(0)

# Test memory space module
if pygb.settings.DEBUG:
    MemoryPoolTest.run_test()
