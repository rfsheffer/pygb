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

from ctypes import c_ubyte, c_ushort, Union, Structure
from pygb.settings import DEBUG

"""
 A and F REGISTERS
"""


class AF(Structure):
    _fields_ = [("f", c_ubyte), ("a", c_ubyte)]


class AFU(Union):
    _fields_ = [("afu", AF), ("af", c_ushort)]


_af = AFU()


def get_a():
    return _af.afu.a


def set_a(val):
    _af.afu.a = val


def get_f():
    return _af.afu.f


def set_f(val):
    _af.afu.f = val


def get_af():
    return _af.af


def set_af(val):
    _af.af = val


"""
 B and C REGISTERS
"""


class BC(Structure):
    _fields_ = [("c", c_ubyte), ("b", c_ubyte)]


class BCU(Union):
    _fields_ = [("bcu", BC), ("bc", c_ushort)]


_bc = BCU()


def get_b():
    return _bc.bcu.b


def set_b(val):
    _bc.bcu.b = val


def get_c():
    return _bc.bcu.c


def set_c(val):
    _bc.bcu.c = val


def get_bc():
    return _bc.bc


def set_bc(val):
    _bc.bc = val


"""
 D and E REGISTERS
"""


class DE(Structure):
    _fields_ = [("e", c_ubyte), ("d", c_ubyte)]


class DEU(Union):
    _fields_ = [("deu", DE), ("de", c_ushort)]


_de = DEU()


def get_d():
    return _de.deu.d


def set_d(val):
    _de.deu.d = val


def get_e():
    return _de.deu.e


def set_e(val):
    _de.deu.e = val


def get_de():
    return _de.de


def set_de(val):
    _de.de = val


"""
 H and L REGISTERS
"""


class HL(Structure):
    _fields_ = [("l", c_ubyte), ("h", c_ubyte)]


class HLU(Union):
    _fields_ = [("hlu", HL), ("hl", c_ushort)]


_hl = HLU()


def get_h():
    return _hl.hlu.h


def set_h(val):
    _hl.hlu.h = val


def get_l():
    return _hl.hlu.l


def set_l(val):
    _hl.hlu.l = val


def get_hl():
    return _hl.hl


def set_hl(val):
    _hl.hl = val


"""
 Stack Pointer
"""
sp = 0

"""
 Program Counter
"""
pc = 0


class RegistersException(Exception):
    """
    Registers exception
    """
    pass


def test_registers():
    """
    Run tests on the registers
    """
    set_f(0x01)
    set_af(0)
    set_a(0xBE)
    set_f(get_f() + 0xEF)
    if get_af() != 0xBEEF:
        raise RegistersException('Bad value of AF! 0x{:X} should be 0xBEEF'.format(get_af()))

    set_c(0x01)
    set_bc(0)
    set_b(0xBE)
    set_c(get_c() + 0xEF)
    if get_bc() != 0xBEEF:
        raise RegistersException('Bad value of BC! 0x{:X} should be 0xBEEF'.format(get_bc()))

    set_e(0x01)
    set_de(0)
    set_d(0xBE)
    set_e(get_e() + 0xEF)
    if get_de() != 0xBEEF:
        raise RegistersException('Bad value of DE! 0x{:X} should be 0xBEEF'.format(get_de()))

    set_l(0x01)
    set_hl(0)
    set_h(0xBE)
    set_l(get_l() + 0xEF)
    if get_hl() != 0xBEEF:
        raise RegistersException('Bad value of HL! 0x{:X} should be 0xBEEF'.format(get_hl()))


if DEBUG:
    test_registers()
