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

from ctypes import c_ubyte, c_ushort, Union, Structure
from pygb.settings import DEBUG


# C Type Declarations
class AF(Structure):
    _fields_ = [("f", c_ubyte), ("a", c_ubyte)]


class AFU(Union):
    _fields_ = [("afu", AF), ("af", c_ushort)]


class BC(Structure):
    _fields_ = [("c", c_ubyte), ("b", c_ubyte)]


class BCU(Union):
    _fields_ = [("bcu", BC), ("bc", c_ushort)]


class DE(Structure):
    _fields_ = [("e", c_ubyte), ("d", c_ubyte)]


class DEU(Union):
    _fields_ = [("deu", DE), ("de", c_ushort)]


class HL(Structure):
    _fields_ = [("l", c_ubyte), ("h", c_ubyte)]


class HLU(Union):
    _fields_ = [("hlu", HL), ("hl", c_ushort)]


class RegisterBank:
    """
    Register Bank
    """
    def __init__(self):
        self._af = AFU()
        self._bc = BCU()
        self._de = DEU()
        self._hl = HLU()
        self._sp = 0
        self._pc = 0

    def do_inc(self, val):
        """
        On increment, certain register flags get set
        :param val: The value to increment
        :return: The value after being incremented
        """
        self.set_half_carry_flag((val & 0x0F) == 0x0F)
        val += 1
        self.set_zero_flag(val == 0)
        self.set_subtract_flag(False)
        return val

    """
     A and F REGISTERS
    """
    def get_a(self):
        return self._af.afu.a

    def set_a(self, val):
        self._af.afu.a = val

    def inc_a(self):
        self._af.afu.a = self.do_inc(self._af.afu.a)
        return self._af.afu.a

    def get_f(self):
        return self._af.afu.f

    def set_f(self, val):
        self._af.afu.f = val
        return self._af.afu.f

    def inc_f(self):
        self._af.afu.f = self.do_inc(self._af.afu.f)
        return self._af.afu.f

    def get_af(self):
        return self._af.af

    def set_af(self, val):
        self._af.af = val

    def get_zero_flag(self):
        """
        Zero Flag (Z)
        This bit is set when the result of a math operation
        is zero or two values match when using the CP
        instruction.
        """
        return 0x80 & self.get_f()

    def set_zero_flag(self, state):
        if state:
            self.set_f(self.get_f() | 0x80)
        else:
            self.set_f(self.get_f() ^ 0x80)

    def get_subtract_flag(self):
        """
        Subtract Flag (N)
        This bit is set if a subtraction was performed in the
        last math instruction.
        """
        return 0x40 & self.get_f()

    def set_subtract_flag(self, state):
        if state:
            self.set_f(self.get_f() | 0x40)
        else:
            self.set_f(self.get_f() ^ 0x40)

    def get_half_carry_flag(self):
        """
        Half Carry Flag (H)
        This bit is set if a carry occurred from the lower
        nibble in the last math operation.
        """
        return 0x20 & self.get_f()

    def set_half_carry_flag(self, state):
        if state:
            self.set_f(self.get_f() | 0x20)
        else:
            self.set_f(self.get_f() ^ 0x20)

    def get_carry_flag(self):
        """
        Half Carry Flag (C)
        This bit is set if a carry occurred from the last
        math operation or if register A is the smaller value
        when executing the CP instruction.
        """
        return 0x10 & self.get_f()

    def set_carry_flag(self, state):
        if state:
            self.set_f(self.get_f() | 0x10)
        else:
            self.set_f(self.get_f() ^ 0x10)

    """
     B and C REGISTERS
    """
    def get_b(self):
        return self._bc.bcu.b

    def set_b(self, val):
        self._bc.bcu.b = val

    def inc_b(self):
        self._bc.bcu.b = self.do_inc(self._bc.bcu.b)
        return self._bc.bcu.b

    def get_c(self):
        return self._bc.bcu.c

    def set_c(self, val):
        self._bc.bcu.c = val

    def inc_c(self):
        self._bc.bcu.c = self.do_inc(self._bc.bcu.c)
        return self._bc.bcu.c

    def get_bc(self):
        return self._bc.bc

    def set_bc(self, val):
        self._bc.bc = val

    """
     D and E REGISTERS
    """
    def get_d(self):
        return self._de.deu.d

    def set_d(self, val):
        self._de.deu.d = val

    def inc_d(self):
        self._de.deu.d = self.do_inc(self._de.deu.d)
        return self._de.deu.d

    def get_e(self):
        return self._de.deu.e

    def set_e(self, val):
        self._de.deu.e = val

    def inc_e(self):
        self._de.deu.e = self.do_inc(self._de.deu.e)
        return self._de.deu.e

    def get_de(self):
        return self._de.de

    def set_de(self, val):
        self._de.de = val

    """
     H and L REGISTERS
    """
    def get_h(self):
        return self._hl.hlu.h

    def set_h(self, val):
        self._hl.hlu.h = val

    def inc_h(self):
        self._hl.hlu.h = self.do_inc(self._hl.hlu.h)
        return self._hl.hlu.h

    def get_l(self):
        return self._hl.hlu.l

    def set_l(self, val):
        self._hl.hlu.l = val

    def inc_l(self):
        self._hl.hlu.l = self.do_inc(self._hl.hlu.l)
        return self._hl.hlu.l

    def get_hl(self):
        return self._hl.hl

    def set_hl(self, val):
        self._hl.hl = val

    """
     Stack Pointer
    """
    def get_sp(self):
        return self._sp

    def set_sp(self, val):
        self._sp = val

    """
     Program Counter
    """
    def get_pc(self):
        """
        Get the current program counter value
        :return: The current program counter value
        """
        return self._pc

    def inc_pc(self, num=1):
        """
        Increment the program counter
        :param num: Num steps
        :return: The program counter value before increment
        """
        pc_out = self._pc
        self._pc += num
        return pc_out

    def set_pc(self, val):
        """
        Explicitly set the program counter value
        :param val: The value to be set as the current program counter
        """
        self._pc = val


class RegistersException(Exception):
    """
    Registers exception
    """
    pass


def test_registers():
    """
    Run tests on the registers
    """
    registers = RegisterBank()
    registers.set_f(0x01)
    registers.set_af(0)
    registers.set_a(0xBE)
    registers.set_f(registers.get_f() + 0xEF)
    if registers.get_af() != 0xBEEF:
        raise RegistersException('Bad value of AF! 0x{:X} should be 0xBEEF'.format(registers.get_af()))

    registers.set_c(0x01)
    registers.set_bc(0)
    registers.set_b(0xBE)
    registers.set_c(registers.get_c() + 0xEF)
    if registers.get_bc() != 0xBEEF:
        raise RegistersException('Bad value of BC! 0x{:X} should be 0xBEEF'.format(registers.get_bc()))

    registers.set_e(0x01)
    registers.set_de(0)
    registers.set_d(0xBE)
    registers.set_e(registers.get_e() + 0xEF)
    if registers.get_de() != 0xBEEF:
        raise RegistersException('Bad value of DE! 0x{:X} should be 0xBEEF'.format(registers.get_de()))

    registers.set_l(0x01)
    registers.set_hl(0)
    registers.set_h(0xBE)
    registers.set_l(registers.get_l() + 0xEF)
    if registers.get_hl() != 0xBEEF:
        raise RegistersException('Bad value of HL! 0x{:X} should be 0xBEEF'.format(registers.get_hl()))


if DEBUG:
    test_registers()

# SPEED TESTS, CLEARLY THE CTYPES VERSION IS CHEAPER THAN BIT SHIFTING.
# import timeit, dis
# class RegisterBank2:
#     def __init__(self):
#         self.a = 0
#         self.f = 0
#
#         self.b = 0
#         self.c = 0
#
#         self.d = 0
#         self.e = 0
#
#         self.h = 0
#         self.l = 0
#
#     def get_af(self):
#         return (self.a << 8) | self.f
#
#     def set_af(self, val):
#         self.f = (0x00FF & val)
#         self.a = (0xFF00 & val) >> 8
#
# regs = RegisterBank()
# regs2 = RegisterBank2()
#
# regs2.set_af(0xBEEF)
# if regs2.a != 0xBE:
#     raise Exception()
# if regs2.f != 0xEF:
#     raise Exception()
#
#
# def run_speed_test1():
#     for i in range(0, 90000):
#         regs.set_af(0)
#         regs.set_af(0xBEEF)
#         regs.get_af()
#
#
# def run_speed_test2():
#     for i in range(0, 90000):
#         regs2.set_af(0)
#         regs2.set_af(0xBEEF)
#         regs2.get_af()
#
# print("Running against C-Types version")
# start_time = timeit.default_timer()
# run_speed_test1()
# print(timeit.default_timer() - start_time)
#
# print("Running against Bit shift version")
# start_time = timeit.default_timer()
# run_speed_test2()
# print(timeit.default_timer() - start_time)
#
# print(dis.dis(regs.set_af))
# print('----------')
# print(dis.dis(regs2.set_af))
