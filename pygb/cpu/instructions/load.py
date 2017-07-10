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

# ------------------------------------------------------------------
# LOAD into C


def ld_c_d(inst, reg, mem, debug):
    """ Load D into C """
    reg.set_c(reg.get_d())
    if debug:
        print(inst.disassembly)


def ld_c_e(inst, reg, mem, debug):
    """ Load E into C """
    reg.set_c(reg.get_e())
    if debug:
        print(inst.disassembly)


# ------------------------------------------------------------------
# LOAD into D


def ld_d_a(inst, reg, mem, debug):
    """ Load A into D """
    reg.set_d(reg.get_a())
    if debug:
        print(inst.disassembly)


def ld_d_b(inst, reg, mem, debug):
    """ Load B into D """
    reg.set_d(reg.get_b())
    if debug:
        print(inst.disassembly)


def ld_d_c(inst, reg, mem, debug):
    """ Load C into D """
    reg.set_d(reg.get_c())
    if debug:
        print(inst.disassembly)


def ld_d_e(inst, reg, mem, debug):
    """ Load E into D """
    reg.set_d(reg.get_e())
    if debug:
        print(inst.disassembly)


def ld_d_l(inst, reg, mem, debug):
    """ Load L into D """
    reg.set_d(reg.get_l())
    if debug:
        print(inst.disassembly)


def ld_d_hlp(inst, reg, mem, debug):
    """ Load (HL) into D """
    reg.set_d(mem.read_byte(reg.get_hl()))
    if debug:
        print(inst.disassembly)


# ------------------------------------------------------------------
# LOAD into E


def ld_e_b(inst, reg, mem, debug):
    """ Load B into E """
    reg.set_e(reg.get_b())
    if debug:
        print(inst.disassembly)


# ------------------------------------------------------------------
# LOAD into L


def ld_l_h(inst, reg, mem, debug):
    """ Load H into L """
    reg.set_l(reg.get_h())
    if debug:
        print(inst.disassembly)


# ------------------------------------------------------------------
# LOAD into DE


def ld_de_nn(inst, reg, mem, debug):
    """ Load NN into DE """
    operand = mem.read_short(reg.get_pc())
    reg.inc_pc(2)
    reg.set_de(operand)
    if debug:
        print(inst.disassembly % operand)
