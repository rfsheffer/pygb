"""
Gameboy Emulator Written in Python

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


class Capabilities:
    """
    The capabilities of the Gameboy main memory
    """
    pass


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
MemoryLocations.print_mem_locations()


class MemoryException(Exception):
    """
    Memory Pool exception
    """
    pass


class MemoryPool:
    """
    Memory Pool Object for accessing the Gameboy memory space
    """

    # Max memory address space for gameboy
    MAX_POOL_SIZE = 0xFFFF

    def __init__(self):
        self.mem = None
        self.mv = None
        self.reset()

    def reset(self):
        """
        Zero all memory in the pool
        """
        if self.mv is not None:
            self.mv.release()
        self.mem = bytearray(MemoryPool.MAX_POOL_SIZE)
        self.mv = memoryview(self.mem)

    @staticmethod
    def check_address(address):
        """
        Check that the address is valid
        :param address: The address changed
        """
        if address < 0 or address >= MemoryPool.MAX_POOL_SIZE:
            raise MemoryException('Invalid Memory Address beyond memory address space! {0}')

    def read_byte(self, address):
        """
        Read a byte from this pools memory space
        :param address: The address to read.
        :return:
        """
        self.check_address(address)
        return self.mem[address]

    def read_short(self, address):
        self.check_address(address)
        self.check_address(address + 1)
        return int.from_bytes(self.mv[address:address + 2].tobytes(), byteorder='big')

    def write_byte(self, address, byte):
        self.check_address(address)
        self.mem[address] = byte
        self.handle_echo_space(address, byte.to_bytes(1, byteorder='big'))

    def write_short(self, address, short):
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

memory_pool = MemoryPool()


class MemoryPoolTest:
    class MemoryPoolTestException(Exception):
        pass

    """
    Gameboy Memory Space tests
    """
    @staticmethod
    def run_test():
        MemoryPoolTest.echo_space_test()

    @staticmethod
    def echo_space_test():
        memory_pool.reset()

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

        memory_pool.reset()

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

        memory_pool.reset()

        # SHORT CHECK
        # Write to the start of the internal mem, except it to end up in the echo space
        memory_pool.write_short(MemoryLocations.internal_ram_addr, 0xDEAD)
        if memory_pool.read_short(MemoryLocations.echo_internal_addr) != 0xDEAD:
            raise MemoryPoolTest.MemoryPoolTestException('Write Short: Internal mem start did not get written to '
                                                         'correctly!')

        # Write to the farthest address into the internal ram, expect the end of echo to contain the value
        memory_pool.write_short(max_im_addr - 2, 0xDEAD)
        if memory_pool.read_short(MemoryLocations.sprite_attrib_mem_addr - 2) != 0xDEAD:
            raise MemoryPoolTest.MemoryPoolTestException('Echo mem space end did not get written to correctly!')

        memory_pool.reset()

        # Write to the start of the echo space, expect it on internal
        memory_pool.write_short(MemoryLocations.echo_internal_addr, 0xDEAD)
        if memory_pool.read_short(MemoryLocations.internal_ram_addr) != 0xDEAD:
            raise MemoryPoolTest.MemoryPoolTestException('Write Short: Internal mem space start did not get written to'
                                                         ' correctly!')

        # Write to the end of the echo space, expect it on internal
        memory_pool.write_short(MemoryLocations.sprite_attrib_mem_addr - 2, 0xDEAD)
        if memory_pool.read_short(max_im_addr - 2) != 0xDEAD:
            raise MemoryPoolTest.MemoryPoolTestException('Write Short: Internal mem space end did not get written to '
                                                         'correctly!')

        memory_pool.reset()

# Test memory space module
MemoryPoolTest.run_test()
