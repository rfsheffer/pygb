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

'''
------------------------------------------------------------------
LOAD CALLS 8bit or 16bit via function swap
'''


def ld_r1_r2(inst, reg, mem):
    """ Put value r2 into r1. """
    read_func = mem.read_byte
    if inst.operand_len == 2:
        read_func = mem.read_short

    if inst.r1[1]:
        # r2 to (r1)
        val = reg.get_reg(inst.r2[0])
        if inst.r2[1]:
            # (r2) to (r1)
            val = read_func(val)
        mem.write_byte(reg.get_reg(inst.r1[0]), val)
    elif inst.r2[1]:
        # (r2) to r1
        val = read_func(reg.get_reg(inst.r2[0]))
        reg.set_reg(inst.r1[0], val)
    else:
        # General r2 to r1
        reg.set_reg(inst.r1[0], reg.get_reg(inst.r2[0]))


def ldd_hlp_a(inst, reg, mem):
    """ load A into (HL) then decrement HL """
    mem.write_byte(reg.get_hl(), reg.get_a())
    reg.dec_hl()


# def ld_r1_nn(inst, reg, mem):
#     """ Put value NN into R1 """
#     value = mem.read_short(reg.get_reg(inst.r2[0]))
#
#     if inst.r1[0] == IReg.REGISTER_BC:
#         reg.set_bc(value)
#     elif inst.r1[0] == IReg.REGISTER_DE:
#         reg.set_de(value)
#     elif inst.r1[0] == IReg.REGISTER_HL:
#         reg.set_hl(value)
#     elif inst.r1[0] == IReg.REGISTER_SP:
#         reg.set_sp(value)
