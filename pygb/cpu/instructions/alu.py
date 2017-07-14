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
from pygb.cpu.registers import IReg


def inc_a(inst, reg, mem, debug):
    """ Increment register A """
    reg.inc_a()
    if debug:
        print(inst.disassembly)


def inc_b(inst, reg, mem, debug):
    """ Increment register B """
    reg.inc_b()
    if debug:
        print(inst.disassembly)


def inc_c(inst, reg, mem, debug):
    """ Increment register C """
    reg.inc_c()
    if debug:
        print(inst.disassembly)


def inc_d(inst, reg, mem, debug):
    """ Increment register D """
    reg.inc_d()
    if debug:
        print(inst.disassembly)


def inc_e(inst, reg, mem, debug):
    """ Increment register E """
    reg.inc_e()
    if debug:
        print(inst.disassembly)


def inc_h(inst, reg, mem, debug):
    """ Increment register H """
    reg.inc_h()
    if debug:
        print(inst.disassembly)


def inc_l(inst, reg, mem, debug):
    """ Increment register L """
    reg.inc_l()
    if debug:
        print(inst.disassembly)


def inc_hlp(inst, reg, mem, debug):
    """ Increment register (HL) """
    mem.write_byte(reg.get_hl(), reg.do_inc(mem.read_byte(reg.get_hl())))
    if debug:
        print(inst.disassembly)


'''
------------------------------------------------------------------
BITWISE OPERATORS
'''


def xor_n(inst, reg, mem, debug):
    debug_val = 0

    def xor_a(value):
        reg.set_a(reg.get_a() ^ value)
        # Reset all flags
        reg.set_f(0)
        # Set zero flag
        if reg.get_a() == 0:
            reg.set_zero_flag(True)

    if inst.reg_r1[0] == IReg.REGISTER_A:
        xor_a(reg.get_a())
    elif inst.reg_r1[0] == IReg.REGISTER_B:
        xor_a(reg.get_b())
    elif inst.reg_r1[0] == IReg.REGISTER_C:
        xor_a(reg.get_c())
    elif inst.reg_r1[0] == IReg.REGISTER_D:
        xor_a(reg.get_d())
    elif inst.reg_r1[0] == IReg.REGISTER_E:
        xor_a(reg.get_e())
    elif inst.reg_r1[0] == IReg.REGISTER_H:
        xor_a(reg.get_h())
    elif inst.reg_r1[0] == IReg.REGISTER_L:
        xor_a(reg.get_l())
    elif inst.reg_r1[0] == IReg.REGISTER_HL:
        xor_a(mem.read_byte(reg.get_hl()))
    elif inst.reg_r1[0] == IReg.REGISTER_PC:
        debug_val = mem.read_byte(reg.get_pc())
        reg.inc_pc(1)
        xor_a(debug_val)

    if debug:
        if inst.reg_r1[0] == IReg.REGISTER_PC:
            print(inst.disassembly % debug_val)
        else:
            print(inst.disassembly)
