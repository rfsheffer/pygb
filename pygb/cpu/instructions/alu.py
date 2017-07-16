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


def inc_r1(inst, reg, mem):
    """ Increment register 1 """
    if inst.r1[1]:
        # inc (r1)
        val = mem.read_byte(reg.get_reg(inst.r1[0]))
        mem.write_byte(reg.get_reg(inst.r1[0]), reg.do_inc(val))
    else:
        # inc r1
        reg.inc_reg(inst.r1[0])


def dec_r1(inst, reg, mem):
    """ Decrement register 1 """
    if inst.r1[1]:
        # inc (r1)
        val = mem.read_byte(reg.get_reg(inst.r1[0]))
        mem.write_byte(reg.get_reg(inst.r1[0]), reg.do_dec(val))
    else:
        # inc r1
        reg.dec_reg(inst.r1[0])



def inc_b(inst, reg, mem):
    """ Increment register B """
    reg.inc_b()


def inc_c(inst, reg, mem):
    """ Increment register C """
    reg.inc_c()


def inc_d(inst, reg, mem):
    """ Increment register D """
    reg.inc_d()


def inc_e(inst, reg, mem):
    """ Increment register E """
    reg.inc_e()


def inc_h(inst, reg, mem):
    """ Increment register H """
    reg.inc_h()


def inc_l(inst, reg, mem):
    """ Increment register L """
    reg.inc_l()


def inc_hlp(inst, reg, mem):
    """ Increment register (HL) """
    mem.write_byte(reg.get_hl(), reg.do_inc(mem.read_byte(reg.get_hl())))


'''
------------------------------------------------------------------
BITWISE OPERATORS
'''


def xor_n(inst, reg, mem):
    def xor_a(value):
        reg.set_a(reg.get_a() ^ value)
        # Reset all flags
        reg.set_f(0)
        # Set zero flag
        if reg.get_a() == 0:
            reg.set_zero_flag(True)

    if inst.r1[1]:
        xor_a(mem.read_byte(reg.get_reg(inst.r1[0])))
    else:
        xor_a(reg.get_reg(inst.r1[0]))
