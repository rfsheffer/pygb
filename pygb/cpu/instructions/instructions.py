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

import pygb.cpu.instructions.load
import pygb.cpu.instructions.misc
import pygb.cpu.instructions.jump
import pygb.cpu.instructions.alu
from pygb.cpu.registers import IReg


class Instruction:
    """
    An Instruction of the CPU
    """
    def __init__(self,
                 disassembly:str,
                 cycles,
                 execute,
                 r1=None, r2=None,
                 operand_len=0,
                 changes_pc=False):
        # For convenience and debug, the disassembly
        self.disassembly = disassembly

        # The number of clock cycles (1 machine cycle == 4 clock cycles)
        # The GB CPU runs at 4.19MHz, 4 cycles == 4.19MHz, 1 NOP is a complete cycle
        self.cycles = cycles

        # The function to execute
        self.execute = execute

        # Registers to change, left side and right side
        # These values are a tuple : (register_index:int, is_pointer:bool)
        self.r1 = r1
        self.r2 = r2

        # If this instruction requires an immediate value
        self.operand_len = operand_len

        # Set to true if the PC is altered by the instruction, and the CPU should continue execution without
        # post incrementing the PC over operands. Used by JP commands.
        self.changes_pc = changes_pc


# List of all instructions in op-code order
instructions = [
    Instruction("NOP",           4,  pygb.cpu.instructions.misc.nop),   # 0x00
    Instruction("LD BC, 0x%04X", 12, pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_BC, False), (IReg.REGISTER_PC, True), 2),   # 0x01
    Instruction("Unknown : 02",  0,  pygb.cpu.instructions.misc.nop),   # 0x02
    Instruction("Unknown : 03",  0,  pygb.cpu.instructions.misc.nop),   # 0x03
    Instruction("INC B",         4,  pygb.cpu.instructions.alu.inc_r1, (IReg.REGISTER_B, False)),   # 0x04
    Instruction("DEC B",         4,  pygb.cpu.instructions.alu.dec_r1, (IReg.REGISTER_B, False)),   # 0x05
    Instruction("LD B, 0x%02X",  8,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_B, False), (IReg.REGISTER_PC, True), 1),   # 0x06
    Instruction("Unknown : 07",  0,  pygb.cpu.instructions.misc.nop),   # 0x07
    Instruction("Unknown : 08",  0,  pygb.cpu.instructions.misc.nop),   # 0x08
    Instruction("Unknown : 09",  0,  pygb.cpu.instructions.misc.nop),   # 0x09
    Instruction("LD A, (BC)",    8,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_A, False), (IReg.REGISTER_BC, True)),   # 0x0A
    Instruction("Unknown : 0B",  0,  pygb.cpu.instructions.misc.nop),   # 0x0B
    Instruction("INC C",         4,  pygb.cpu.instructions.alu.inc_r1, (IReg.REGISTER_C, False)),   # 0x0C
    Instruction("DEC C",         4,  pygb.cpu.instructions.alu.dec_r1, (IReg.REGISTER_C, False)),   # 0x0D
    Instruction("LD C, 0x%02X",  8,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_C, False), (IReg.REGISTER_PC, True), 1),   # 0x0E
    Instruction("Unknown : 0F",  0,  pygb.cpu.instructions.misc.nop),   # 0x0F
    Instruction("Unknown : 10",  0,  pygb.cpu.instructions.misc.nop),   # 0x10
    Instruction("LD DE, 0x%04X", 12, pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_DE, False), (IReg.REGISTER_PC, True), 2),   # 0x11
    Instruction("Unknown : 12",  0,  pygb.cpu.instructions.misc.nop),   # 0x12
    Instruction("Unknown : 13",  0,  pygb.cpu.instructions.misc.nop),   # 0x13
    Instruction("INC D",         4,  pygb.cpu.instructions.alu.inc_r1, (IReg.REGISTER_D, False)),   # 0x14
    Instruction("DEC D",         4,  pygb.cpu.instructions.alu.dec_r1, (IReg.REGISTER_D, False)),   # 0x15
    Instruction("LD D, 0x%02X",  8,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_D, False), (IReg.REGISTER_PC, True), 1),   # 0x16
    Instruction("Unknown : 17",  0,  pygb.cpu.instructions.misc.nop),   # 0x17
    Instruction("Unknown : 18",  0,  pygb.cpu.instructions.misc.nop),   # 0x18
    Instruction("Unknown : 19",  0,  pygb.cpu.instructions.misc.nop),   # 0x19
    Instruction("LD A, (DE)",    8,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_A, False), (IReg.REGISTER_DE, True)),   # 0x1A
    Instruction("Unknown : 1B",  0,  pygb.cpu.instructions.misc.nop),   # 0x1B
    Instruction("INC E",         4,  pygb.cpu.instructions.alu.inc_r1, (IReg.REGISTER_E, False)),   # 0x1C
    Instruction("DEC E",         4,  pygb.cpu.instructions.alu.dec_r1, (IReg.REGISTER_E, False)),   # 0x1D
    Instruction("LD E, 0x%02X",  8,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_E, False), (IReg.REGISTER_PC, True), 1),   # 0x1E
    Instruction("Unknown : 1F",  0,  pygb.cpu.instructions.misc.nop),   # 0x1F
    Instruction("JR NZ, 0x%02X", 8,  pygb.cpu.instructions.jump.jr_nz_n, (IReg.REGISTER_PC, True), None, 1, True),   # 0x20
    Instruction("LD HL, 0x%04X", 12, pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_HL, False), (IReg.REGISTER_PC, True), 2),   # 0x21
    Instruction("Unknown : 22",  0,  pygb.cpu.instructions.misc.nop),   # 0x22
    Instruction("Unknown : 23",  0,  pygb.cpu.instructions.misc.nop),   # 0x23
    Instruction("INC H",         4,  pygb.cpu.instructions.alu.inc_r1, (IReg.REGISTER_H, False)),   # 0x24
    Instruction("DEC H",         4,  pygb.cpu.instructions.alu.dec_r1, (IReg.REGISTER_H, False)),   # 0x25
    Instruction("LD H, 0x%02X",  8,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_H, False), (IReg.REGISTER_PC, True), 1),   # 0x26
    Instruction("Unknown : 27",  0,  pygb.cpu.instructions.misc.nop),   # 0x27
    Instruction("Unknown : 28",  0,  pygb.cpu.instructions.misc.nop),   # 0x28
    Instruction("Unknown : 29",  0,  pygb.cpu.instructions.misc.nop),   # 0x29
    Instruction("Unknown : 2A",  0,  pygb.cpu.instructions.misc.nop),   # 0x2A
    Instruction("Unknown : 2B",  0,  pygb.cpu.instructions.misc.nop),   # 0x2B
    Instruction("INC L",         4,  pygb.cpu.instructions.alu.inc_r1, (IReg.REGISTER_L, False)),   # 0x2C
    Instruction("DEC L",         4,  pygb.cpu.instructions.alu.dec_r1, (IReg.REGISTER_L, False)),   # 0x2D
    Instruction("LD L, 0x%02X",  8,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_L, False), (IReg.REGISTER_PC, True), 1),   # 0x2E
    Instruction("Unknown : 2F",  0,  pygb.cpu.instructions.misc.nop),   # 0x2F
    Instruction("Unknown : 30",  0,  pygb.cpu.instructions.misc.nop),   # 0x30
    Instruction("LD SP, 0x%04X", 12, pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_SP, False), (IReg.REGISTER_PC, True), 2),   # 0x31
    Instruction("LDD (HL), A",   8,  pygb.cpu.instructions.load.ldd_hlp_a, (IReg.REGISTER_HL, True), (IReg.REGISTER_A, False)),   # 0x32
    Instruction("Unknown : 33",  0,  pygb.cpu.instructions.misc.nop),   # 0x33
    Instruction("INC (HL)",      8,  pygb.cpu.instructions.alu.inc_r1, (IReg.REGISTER_HL, True)),   # 0x34
    Instruction("DEC (HL)",      8,  pygb.cpu.instructions.alu.dec_r1, (IReg.REGISTER_HL, True)),   # 0x35
    Instruction("LD (HL), 0x%02X",12,pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_HL, True), (IReg.REGISTER_PC, True), 1),   # 0x36
    Instruction("Unknown : 37",  0,  pygb.cpu.instructions.misc.nop),   # 0x37
    Instruction("Unknown : 38",  0,  pygb.cpu.instructions.misc.nop),   # 0x38
    Instruction("Unknown : 39",  0,  pygb.cpu.instructions.misc.nop),   # 0x39
    Instruction("Unknown : 3A",  0,  pygb.cpu.instructions.misc.nop),   # 0x3A
    Instruction("Unknown : 3B",  0,  pygb.cpu.instructions.misc.nop),   # 0x3B
    Instruction("INC A",         4,  pygb.cpu.instructions.alu.inc_r1, (IReg.REGISTER_A, False)),   # 0x3C
    Instruction("DEC A",         4,  pygb.cpu.instructions.alu.dec_r1, (IReg.REGISTER_A, False)),   # 0x3D
    Instruction("LD A, 0x%02X",  8,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_A, False), (IReg.REGISTER_PC, True), 1),   # 0x3E
    Instruction("Unknown : 3F",  0,  pygb.cpu.instructions.misc.nop),   # 0x3F
    Instruction("LD B, B",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_B, False), (IReg.REGISTER_B, False)),   # 0x40
    Instruction("LD B, C",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_B, False), (IReg.REGISTER_C, False)),   # 0x41
    Instruction("LD B, D",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_B, False), (IReg.REGISTER_D, False)),   # 0x42
    Instruction("LD B, E",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_B, False), (IReg.REGISTER_E, False)),   # 0x43
    Instruction("LD B, H",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_B, False), (IReg.REGISTER_H, False)),   # 0x44
    Instruction("LD B, L",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_B, False), (IReg.REGISTER_L, False)),   # 0x45
    Instruction("LD B, (HL)",    8,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_B, False), (IReg.REGISTER_HL, True)),   # 0x46
    Instruction("LD B, A",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_B, False), (IReg.REGISTER_A, False)),   # 0x47
    Instruction("LD C, B",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_C, False), (IReg.REGISTER_B, False)),   # 0x48
    Instruction("LD C, C",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_C, False), (IReg.REGISTER_C, False)),   # 0x49
    Instruction("LD C, D",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_C, False), (IReg.REGISTER_D, False)),   # 0x4A
    Instruction("LD C, E",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_C, False), (IReg.REGISTER_E, False)),   # 0x4B
    Instruction("LD C, H",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_C, False), (IReg.REGISTER_H, False)),   # 0x4C
    Instruction("LD C, L",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_C, False), (IReg.REGISTER_L, False)),   # 0x4D
    Instruction("LD C, (HL)",    8,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_C, False), (IReg.REGISTER_HL, True)),   # 0x4E
    Instruction("LD C, A",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_C, False), (IReg.REGISTER_A, False)),   # 0x4F
    Instruction("LD D, B",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_D, False), (IReg.REGISTER_B, False)),   # 0x50
    Instruction("LD D, C",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_D, False), (IReg.REGISTER_C, False)),   # 0x51
    Instruction("LD D, D",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_D, False), (IReg.REGISTER_D, False)),   # 0x52
    Instruction("LD D, E",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_D, False), (IReg.REGISTER_E, False)),   # 0x53
    Instruction("LD D, H",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_D, False), (IReg.REGISTER_H, False)),   # 0x54
    Instruction("LD D, L",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_D, False), (IReg.REGISTER_L, False)),   # 0x55
    Instruction("LD D, (HL)",    8,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_D, False), (IReg.REGISTER_HL, True)),   # 0x56
    Instruction("LD D, A",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_D, False), (IReg.REGISTER_A, False)),   # 0x57
    Instruction("LD E, B",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_E, False), (IReg.REGISTER_B, False)),   # 0x58
    Instruction("LD E, C",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_E, False), (IReg.REGISTER_C, False)),   # 0x59
    Instruction("LD E, D",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_E, False), (IReg.REGISTER_D, False)),   # 0x5A
    Instruction("LD E, E",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_E, False), (IReg.REGISTER_E, False)),   # 0x5B
    Instruction("LD E, H",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_E, False), (IReg.REGISTER_H, False)),   # 0x5C
    Instruction("LD E, L",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_E, False), (IReg.REGISTER_L, False)),   # 0x5D
    Instruction("LD E, (HL)",    8,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_E, False), (IReg.REGISTER_HL, True)),   # 0x5E
    Instruction("LD E, A",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_E, False), (IReg.REGISTER_A, False)),   # 0x5F
    Instruction("LD H, B",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_H, False), (IReg.REGISTER_B, False)),   # 0x60
    Instruction("LD H, C",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_H, False), (IReg.REGISTER_C, False)),   # 0x61
    Instruction("LD H, D",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_H, False), (IReg.REGISTER_D, False)),   # 0x62
    Instruction("LD H, E",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_H, False), (IReg.REGISTER_E, False)),   # 0x63
    Instruction("LD H, H",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_H, False), (IReg.REGISTER_H, False)),   # 0x64
    Instruction("LD H, L",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_H, False), (IReg.REGISTER_L, False)),   # 0x65
    Instruction("LD H, (HL)",    8,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_H, False), (IReg.REGISTER_HL, True)),   # 0x66
    Instruction("LD H, A",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_H, False), (IReg.REGISTER_A, False)),   # 0x67
    Instruction("LD L, B",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_L, False), (IReg.REGISTER_B, False)),   # 0x68
    Instruction("LD L, C",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_L, False), (IReg.REGISTER_C, False)),   # 0x69
    Instruction("LD L, D",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_L, False), (IReg.REGISTER_D, False)),   # 0x6A
    Instruction("LD L, E",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_L, False), (IReg.REGISTER_E, False)),   # 0x6B
    Instruction("LD L, H",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_L, False), (IReg.REGISTER_H, False)),   # 0x6C
    Instruction("LD L, L",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_L, False), (IReg.REGISTER_L, False)),   # 0x6D
    Instruction("LD L, (HL)",    8,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_L, False), (IReg.REGISTER_HL, True)),   # 0x6E
    Instruction("LD L, A",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_L, False), (IReg.REGISTER_A, False)),   # 0x6F
    Instruction("LD (HL), B",    8,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_HL, True), (IReg.REGISTER_B, False)),   # 0x70
    Instruction("LD (HL), C",    8,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_HL, True), (IReg.REGISTER_C, False)),   # 0x71
    Instruction("LD (HL), D",    8,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_HL, True), (IReg.REGISTER_D, False)),   # 0x72
    Instruction("LD (HL), E",    8,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_HL, True), (IReg.REGISTER_E, False)),   # 0x73
    Instruction("LD (HL), H",    8,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_HL, True), (IReg.REGISTER_H, False)),   # 0x74
    Instruction("LD (HL), L",    8,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_HL, True), (IReg.REGISTER_L, False)),   # 0x75
    Instruction("Unknown : 76",  0,  pygb.cpu.instructions.misc.nop),   # 0x76
    Instruction("Unknown : 77",  0,  pygb.cpu.instructions.misc.nop),   # 0x77
    Instruction("LD A, B",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_A, False), (IReg.REGISTER_B, False)),   # 0x78
    Instruction("LD A, C",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_A, False), (IReg.REGISTER_C, False)),   # 0x79
    Instruction("LD A, D",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_A, False), (IReg.REGISTER_D, False)),   # 0x7A
    Instruction("LD A, E",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_A, False), (IReg.REGISTER_E, False)),   # 0x7B
    Instruction("LD A, H",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_A, False), (IReg.REGISTER_H, False)),   # 0x7C
    Instruction("LD A, L",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_A, False), (IReg.REGISTER_L, False)),   # 0x7D
    Instruction("LD A, (HL)",    8,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_A, False), (IReg.REGISTER_HL, True)),   # 0x7E
    Instruction("LD A, A",       4,  pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_A, False), (IReg.REGISTER_A, False)),   # 0x7F
    Instruction("Unknown : 80",  0,  pygb.cpu.instructions.misc.nop),   # 0x80
    Instruction("Unknown : 81",  0,  pygb.cpu.instructions.misc.nop),   # 0x81
    Instruction("Unknown : 82",  0,  pygb.cpu.instructions.misc.nop),   # 0x82
    Instruction("Unknown : 83",  0,  pygb.cpu.instructions.misc.nop),   # 0x83
    Instruction("Unknown : 84",  0,  pygb.cpu.instructions.misc.nop),   # 0x84
    Instruction("Unknown : 85",  0,  pygb.cpu.instructions.misc.nop),   # 0x85
    Instruction("Unknown : 86",  0,  pygb.cpu.instructions.misc.nop),   # 0x86
    Instruction("Unknown : 87",  0,  pygb.cpu.instructions.misc.nop),   # 0x87
    Instruction("Unknown : 88",  0,  pygb.cpu.instructions.misc.nop),   # 0x88
    Instruction("Unknown : 89",  0,  pygb.cpu.instructions.misc.nop),   # 0x89
    Instruction("Unknown : 8A",  0,  pygb.cpu.instructions.misc.nop),   # 0x8A
    Instruction("Unknown : 8B",  0,  pygb.cpu.instructions.misc.nop),   # 0x8B
    Instruction("Unknown : 8C",  0,  pygb.cpu.instructions.misc.nop),   # 0x8C
    Instruction("Unknown : 8D",  0,  pygb.cpu.instructions.misc.nop),   # 0x8D
    Instruction("Unknown : 8E",  0,  pygb.cpu.instructions.misc.nop),   # 0x8E
    Instruction("Unknown : 8F",  0,  pygb.cpu.instructions.misc.nop),   # 0x8F
    Instruction("Unknown : 90",  0,  pygb.cpu.instructions.misc.nop),   # 0x90
    Instruction("Unknown : 91",  0,  pygb.cpu.instructions.misc.nop),   # 0x91
    Instruction("Unknown : 92",  0,  pygb.cpu.instructions.misc.nop),   # 0x92
    Instruction("Unknown : 93",  0,  pygb.cpu.instructions.misc.nop),   # 0x93
    Instruction("Unknown : 94",  0,  pygb.cpu.instructions.misc.nop),   # 0x94
    Instruction("Unknown : 95",  0,  pygb.cpu.instructions.misc.nop),   # 0x95
    Instruction("Unknown : 96",  0,  pygb.cpu.instructions.misc.nop),   # 0x96
    Instruction("Unknown : 97",  0,  pygb.cpu.instructions.misc.nop),   # 0x97
    Instruction("Unknown : 98",  0,  pygb.cpu.instructions.misc.nop),   # 0x98
    Instruction("Unknown : 99",  0,  pygb.cpu.instructions.misc.nop),   # 0x99
    Instruction("Unknown : 9A",  0,  pygb.cpu.instructions.misc.nop),   # 0x9A
    Instruction("Unknown : 9B",  0,  pygb.cpu.instructions.misc.nop),   # 0x9B
    Instruction("Unknown : 9C",  0,  pygb.cpu.instructions.misc.nop),   # 0x9C
    Instruction("Unknown : 9D",  0,  pygb.cpu.instructions.misc.nop),   # 0x9D
    Instruction("Unknown : 9E",  0,  pygb.cpu.instructions.misc.nop),   # 0x9E
    Instruction("Unknown : 9F",  0,  pygb.cpu.instructions.misc.nop),   # 0x9F
    Instruction("Unknown : A0",  0,  pygb.cpu.instructions.misc.nop),   # 0xA0
    Instruction("Unknown : A1",  0,  pygb.cpu.instructions.misc.nop),   # 0xA1
    Instruction("Unknown : A2",  0,  pygb.cpu.instructions.misc.nop),   # 0xA2
    Instruction("Unknown : A3",  0,  pygb.cpu.instructions.misc.nop),   # 0xA3
    Instruction("Unknown : A4",  0,  pygb.cpu.instructions.misc.nop),   # 0xA4
    Instruction("Unknown : A5",  0,  pygb.cpu.instructions.misc.nop),   # 0xA5
    Instruction("Unknown : A6",  0,  pygb.cpu.instructions.misc.nop),   # 0xA6
    Instruction("Unknown : A7",  0,  pygb.cpu.instructions.misc.nop),   # 0xA7
    Instruction("XOR B",         4,  pygb.cpu.instructions.alu.xor_n, (IReg.REGISTER_B, False)),   # 0xA8
    Instruction("XOR C",         4,  pygb.cpu.instructions.alu.xor_n, (IReg.REGISTER_C, False)),   # 0xA9
    Instruction("XOR D",         4,  pygb.cpu.instructions.alu.xor_n, (IReg.REGISTER_D, False)),   # 0xAA
    Instruction("XOR E",         4,  pygb.cpu.instructions.alu.xor_n, (IReg.REGISTER_E, False)),   # 0xAB
    Instruction("XOR H",         4,  pygb.cpu.instructions.alu.xor_n, (IReg.REGISTER_H, False)),   # 0xAC
    Instruction("XOR L",         4,  pygb.cpu.instructions.alu.xor_n, (IReg.REGISTER_L, False)),   # 0xAD
    Instruction("XOR (HL)",      8,  pygb.cpu.instructions.alu.xor_n, (IReg.REGISTER_HL, True)),   # 0xAE
    Instruction("XOR A",         4,  pygb.cpu.instructions.alu.xor_n, (IReg.REGISTER_A, False)),   # 0xAF
    Instruction("Unknown : B0",  0,  pygb.cpu.instructions.misc.nop),   # 0xB0
    Instruction("Unknown : B1",  0,  pygb.cpu.instructions.misc.nop),   # 0xB1
    Instruction("Unknown : B2",  0,  pygb.cpu.instructions.misc.nop),   # 0xB2
    Instruction("Unknown : B3",  0,  pygb.cpu.instructions.misc.nop),   # 0xB3
    Instruction("Unknown : B4",  0,  pygb.cpu.instructions.misc.nop),   # 0xB4
    Instruction("Unknown : B5",  0,  pygb.cpu.instructions.misc.nop),   # 0xB5
    Instruction("Unknown : B6",  0,  pygb.cpu.instructions.misc.nop),   # 0xB6
    Instruction("Unknown : B7",  0,  pygb.cpu.instructions.misc.nop),   # 0xB7
    Instruction("Unknown : B8",  0,  pygb.cpu.instructions.misc.nop),   # 0xB8
    Instruction("Unknown : B9",  0,  pygb.cpu.instructions.misc.nop),   # 0xB9
    Instruction("Unknown : BA",  0,  pygb.cpu.instructions.misc.nop),   # 0xBA
    Instruction("Unknown : BB",  0,  pygb.cpu.instructions.misc.nop),   # 0xBB
    Instruction("Unknown : BC",  0,  pygb.cpu.instructions.misc.nop),   # 0xBC
    Instruction("Unknown : BD",  0,  pygb.cpu.instructions.misc.nop),   # 0xBD
    Instruction("Unknown : BE",  0,  pygb.cpu.instructions.misc.nop),   # 0xBE
    Instruction("Unknown : BF",  0,  pygb.cpu.instructions.misc.nop),   # 0xBF
    Instruction("Unknown : C0",  0,  pygb.cpu.instructions.misc.nop),   # 0xC0
    Instruction("Unknown : C1",  0,  pygb.cpu.instructions.misc.nop),   # 0xC1
    Instruction("Unknown : C2",  0,  pygb.cpu.instructions.misc.nop),   # 0xC2
    Instruction("JP 0x%04X",     12, pygb.cpu.instructions.jump.jp_nn, (IReg.REGISTER_PC, True), None, 2, True),  # 0xC3
    Instruction("Unknown : C4",  0,  pygb.cpu.instructions.misc.nop),   # 0xC4
    Instruction("Unknown : C5",  0,  pygb.cpu.instructions.misc.nop),   # 0xC5
    Instruction("Unknown : C6",  0,  pygb.cpu.instructions.misc.nop),   # 0xC6
    Instruction("Unknown : C7",  0,  pygb.cpu.instructions.misc.nop),   # 0xC7
    Instruction("Unknown : C8",  0,  pygb.cpu.instructions.misc.nop),   # 0xC8
    Instruction("Unknown : C9",  0,  pygb.cpu.instructions.misc.nop),   # 0xC9
    Instruction("Unknown : CA",  0,  pygb.cpu.instructions.misc.nop),   # 0xCA
    Instruction("Unknown : CB",  0,  pygb.cpu.instructions.misc.nop),   # 0xCB
    Instruction("Unknown : CC",  0,  pygb.cpu.instructions.misc.nop),   # 0xCC
    Instruction("Unknown : CD",  0,  pygb.cpu.instructions.misc.nop),   # 0xCD
    Instruction("Unknown : CE",  0,  pygb.cpu.instructions.misc.nop),   # 0xCE
    Instruction("Unknown : CF",  0,  pygb.cpu.instructions.misc.nop),   # 0xCF
    Instruction("Unknown : D0",  0,  pygb.cpu.instructions.misc.nop),   # 0xD0
    Instruction("Unknown : D1",  0,  pygb.cpu.instructions.misc.nop),   # 0xD1
    Instruction("Unknown : D2",  0,  pygb.cpu.instructions.misc.nop),   # 0xD2
    Instruction("Unknown : D3",  0,  pygb.cpu.instructions.misc.nop),   # 0xD3
    Instruction("Unknown : D4",  0,  pygb.cpu.instructions.misc.nop),   # 0xD4
    Instruction("Unknown : D5",  0,  pygb.cpu.instructions.misc.nop),   # 0xD5
    Instruction("Unknown : D6",  0,  pygb.cpu.instructions.misc.nop),   # 0xD6
    Instruction("Unknown : D7",  0,  pygb.cpu.instructions.misc.nop),   # 0xD7
    Instruction("Unknown : D8",  0,  pygb.cpu.instructions.misc.nop),   # 0xD8
    Instruction("Unknown : D9",  0,  pygb.cpu.instructions.misc.nop),   # 0xD9
    Instruction("Unknown : DA",  0,  pygb.cpu.instructions.misc.nop),   # 0xDA
    Instruction("Unknown : DB",  0,  pygb.cpu.instructions.misc.nop),   # 0xDB
    Instruction("Unknown : DC",  0,  pygb.cpu.instructions.misc.nop),   # 0xDC
    Instruction("Unknown : DD",  0,  pygb.cpu.instructions.misc.nop),   # 0xDD
    Instruction("Unknown : DE",  0,  pygb.cpu.instructions.misc.nop),   # 0xDE
    Instruction("Unknown : DF",  0,  pygb.cpu.instructions.misc.nop),   # 0xDF
    Instruction("Unknown : E0",  0,  pygb.cpu.instructions.misc.nop),   # 0xE0
    Instruction("Unknown : E1",  0,  pygb.cpu.instructions.misc.nop),   # 0xE1
    Instruction("Unknown : E2",  0,  pygb.cpu.instructions.misc.nop),   # 0xE2
    Instruction("Unknown : E3",  0,  pygb.cpu.instructions.misc.nop),   # 0xE3
    Instruction("Unknown : E4",  0,  pygb.cpu.instructions.misc.nop),   # 0xE4
    Instruction("Unknown : E5",  0,  pygb.cpu.instructions.misc.nop),   # 0xE5
    Instruction("Unknown : E6",  0,  pygb.cpu.instructions.misc.nop),   # 0xE6
    Instruction("Unknown : E7",  0,  pygb.cpu.instructions.misc.nop),   # 0xE7
    Instruction("Unknown : E8",  0,  pygb.cpu.instructions.misc.nop),   # 0xE8
    Instruction("Unknown : E9",  0,  pygb.cpu.instructions.misc.nop),   # 0xE9
    Instruction("Unknown : EA",  0,  pygb.cpu.instructions.misc.nop),   # 0xEA
    Instruction("Unknown : EB",  0,  pygb.cpu.instructions.misc.nop),   # 0xEB
    Instruction("Unknown : EC",  0,  pygb.cpu.instructions.misc.nop),   # 0xEC
    Instruction("Unknown : ED",  0,  pygb.cpu.instructions.misc.nop),   # 0xED
    Instruction("XOR 0x%02X",    8,  pygb.cpu.instructions.alu.xor_n, (IReg.REGISTER_PC, True), None, 1),   # 0xEE
    Instruction("Unknown : EF",  0,  pygb.cpu.instructions.misc.nop),   # 0xEF
    Instruction("Unknown : F0",  0,  pygb.cpu.instructions.misc.nop),   # 0xF0
    Instruction("Unknown : F1",  0,  pygb.cpu.instructions.misc.nop),   # 0xF1
    Instruction("Unknown : F2",  0,  pygb.cpu.instructions.misc.nop),   # 0xF2
    Instruction("DI",            4,  pygb.cpu.instructions.misc.nop),   # 0xF3
    Instruction("Unknown : F4",  0,  pygb.cpu.instructions.misc.nop),   # 0xF4
    Instruction("Unknown : F5",  0,  pygb.cpu.instructions.misc.nop),   # 0xF5
    Instruction("Unknown : F6",  0,  pygb.cpu.instructions.misc.nop),   # 0xF6
    Instruction("Unknown : F7",  0,  pygb.cpu.instructions.misc.nop),   # 0xF7
    Instruction("Unknown : F8",  0,  pygb.cpu.instructions.misc.nop),   # 0xF8
    Instruction("Unknown : F9",  0,  pygb.cpu.instructions.misc.nop),   # 0xF9
    Instruction("LD A, 0x%04X",  16, pygb.cpu.instructions.load.ld_r1_r2, (IReg.REGISTER_A, False), (IReg.REGISTER_PC, True), 2),   # 0xFA
    Instruction("EI",            4,  pygb.cpu.instructions.misc.nop),   # 0xFB
    Instruction("Unknown : FC",  0,  pygb.cpu.instructions.misc.nop),   # 0xFC
    Instruction("Unknown : FD",  0,  pygb.cpu.instructions.misc.nop),   # 0xFD
    Instruction("Unknown : FE",  0,  pygb.cpu.instructions.misc.nop),   # 0xFE
    Instruction("Unknown : FF",  0,  pygb.cpu.instructions.misc.nop),   # 0xFF
]
