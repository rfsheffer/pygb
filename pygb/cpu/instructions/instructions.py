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


class Instruction:
    """
    An Instruction of the CPU
    """
    def __init__(self, disassembly, num_operands, cycles, execute):
        # For convenience and debug, the disassembly
        self.disassembly = disassembly

        # Number of operands for this instruction
        self.num_operands = num_operands

        # The number of clock cycles (1 machine cycle == 4 clock cycles)
        self.cycles = cycles

        # The function to execute
        self.execute = execute


# List of all instructions in op-code order
instructions = [
    Instruction("NOP",                 0, 4, pygb.cpu.instructions.misc.nop),   # 0x00
    Instruction("Unknown : 01",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x01
    Instruction("Unknown : 02",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x02
    Instruction("Unknown : 03",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x03
    Instruction("INC B",               0, 0, pygb.cpu.instructions.alu.inc_b),   # 0x04
    Instruction("Unknown : 05",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x05
    Instruction("Unknown : 06",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x06
    Instruction("Unknown : 07",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x07
    Instruction("Unknown : 08",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x08
    Instruction("Unknown : 09",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x09
    Instruction("Unknown : 0A",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x0A
    Instruction("Unknown : 0B",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x0B
    Instruction("INC C",               0, 0, pygb.cpu.instructions.alu.inc_c),   # 0x0C
    Instruction("Unknown : 0D",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x0D
    Instruction("Unknown : 0E",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x0E
    Instruction("Unknown : 0F",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x0F
    Instruction("Unknown : 10",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x10
    Instruction("LD DE 0x%04X",        2, 0, pygb.cpu.instructions.load.ld_de_nn),   # 0x11
    Instruction("Unknown : 12",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x12
    Instruction("Unknown : 13",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x13
    Instruction("INC D",               0, 0, pygb.cpu.instructions.alu.inc_d),   # 0x14
    Instruction("Unknown : 15",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x15
    Instruction("Unknown : 16",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x16
    Instruction("Unknown : 17",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x17
    Instruction("Unknown : 18",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x18
    Instruction("Unknown : 19",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x19
    Instruction("Unknown : 1A",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x1A
    Instruction("Unknown : 1B",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x1B
    Instruction("INC E",               0, 0, pygb.cpu.instructions.alu.inc_e),   # 0x1C
    Instruction("Unknown : 1D",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x1D
    Instruction("Unknown : 1E",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x1E
    Instruction("Unknown : 1F",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x1F
    Instruction("Unknown : 20",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x20
    Instruction("Unknown : 21",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x21
    Instruction("Unknown : 22",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x22
    Instruction("Unknown : 23",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x23
    Instruction("INC H",               0, 0, pygb.cpu.instructions.alu.inc_h),   # 0x24
    Instruction("Unknown : 25",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x25
    Instruction("Unknown : 26",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x26
    Instruction("Unknown : 27",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x27
    Instruction("Unknown : 28",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x28
    Instruction("Unknown : 29",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x29
    Instruction("Unknown : 2A",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x2A
    Instruction("Unknown : 2B",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x2B
    Instruction("INC L",               0, 0, pygb.cpu.instructions.alu.inc_l),   # 0x2C
    Instruction("Unknown : 2D",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x2D
    Instruction("Unknown : 2E",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x2E
    Instruction("Unknown : 2F",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x2F
    Instruction("Unknown : 30",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x30
    Instruction("Unknown : 31",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x31
    Instruction("Unknown : 32",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x32
    Instruction("Unknown : 33",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x33
    Instruction("INC (HL)",            0, 0, pygb.cpu.instructions.alu.inc_hlp),   # 0x34
    Instruction("Unknown : 35",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x35
    Instruction("Unknown : 36",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x36
    Instruction("Unknown : 37",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x37
    Instruction("Unknown : 38",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x38
    Instruction("Unknown : 39",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x39
    Instruction("Unknown : 3A",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x3A
    Instruction("Unknown : 3B",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x3B
    Instruction("INC A",               0, 0, pygb.cpu.instructions.alu.inc_a),   # 0x3C
    Instruction("Unknown : 3D",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x3D
    Instruction("Unknown : 3E",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x3E
    Instruction("Unknown : 3F",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x3F
    Instruction("Unknown : 40",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x40
    Instruction("Unknown : 41",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x41
    Instruction("Unknown : 42",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x42
    Instruction("Unknown : 43",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x43
    Instruction("Unknown : 44",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x44
    Instruction("Unknown : 45",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x45
    Instruction("Unknown : 46",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x46
    Instruction("Unknown : 47",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x47
    Instruction("Unknown : 48",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x48
    Instruction("Unknown : 49",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x49
    Instruction("LD C, D",             0, 0, pygb.cpu.instructions.load.ld_c_d),   # 0x4A
    Instruction("LD C, E",             0, 0, pygb.cpu.instructions.load.ld_c_e),   # 0x4B
    Instruction("Unknown : 4C",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x4C
    Instruction("Unknown : 4D",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x4D
    Instruction("Unknown : 4E",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x4E
    Instruction("Unknown : 4F",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x4F
    Instruction("LD D, B",             0, 0, pygb.cpu.instructions.load.ld_d_b),    # 0x50
    Instruction("Unknown : 51",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x51
    Instruction("Unknown : 52",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x52
    Instruction("LD D, E",             0, 0, pygb.cpu.instructions.load.ld_d_e),   # 0x53
    Instruction("Unknown : 54",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x54
    Instruction("LD D, L",             0, 0, pygb.cpu.instructions.load.ld_d_l),   # 0x55
    Instruction("LD D, (HL)",          0, 0, pygb.cpu.instructions.load.ld_d_hlp),   # 0x56
    Instruction("LD D, A",             0, 0, pygb.cpu.instructions.load.ld_d_a),   # 0x57
    Instruction("LD E, B",             0, 0, pygb.cpu.instructions.load.ld_e_b),   # 0x58
    Instruction("Unknown : 59",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x59
    Instruction("Unknown : 5A",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x5A
    Instruction("Unknown : 5B",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x5B
    Instruction("Unknown : 5C",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x5C
    Instruction("Unknown : 5D",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x5D
    Instruction("Unknown : 5E",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x5E
    Instruction("Unknown : 5F",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x5F
    Instruction("Unknown : 60",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x60
    Instruction("Unknown : 61",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x61
    Instruction("Unknown : 62",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x62
    Instruction("Unknown : 63",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x63
    Instruction("Unknown : 64",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x64
    Instruction("Unknown : 65",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x65
    Instruction("Unknown : 66",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x66
    Instruction("Unknown : 67",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x67
    Instruction("Unknown : 68",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x68
    Instruction("Unknown : 69",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x69
    Instruction("Unknown : 6A",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x6A
    Instruction("Unknown : 6B",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x6B
    Instruction("LD L, H",             0, 0, pygb.cpu.instructions.load.ld_l_h),   # 0x6C
    Instruction("Unknown : 6D",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x6D
    Instruction("Unknown : 6E",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x6E
    Instruction("Unknown : 6F",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x6F
    Instruction("Unknown : 70",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x70
    Instruction("Unknown : 71",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x71
    Instruction("Unknown : 72",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x72
    Instruction("Unknown : 73",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x73
    Instruction("Unknown : 74",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x74
    Instruction("Unknown : 75",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x75
    Instruction("Unknown : 76",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x76
    Instruction("Unknown : 77",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x77
    Instruction("Unknown : 78",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x78
    Instruction("Unknown : 79",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x79
    Instruction("Unknown : 7A",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x7A
    Instruction("Unknown : 7B",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x7B
    Instruction("Unknown : 7C",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x7C
    Instruction("Unknown : 7D",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x7D
    Instruction("Unknown : 7E",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x7E
    Instruction("Unknown : 7F",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x7F
    Instruction("Unknown : 80",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x80
    Instruction("Unknown : 81",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x81
    Instruction("Unknown : 82",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x82
    Instruction("Unknown : 83",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x83
    Instruction("Unknown : 84",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x84
    Instruction("Unknown : 85",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x85
    Instruction("Unknown : 86",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x86
    Instruction("Unknown : 87",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x87
    Instruction("Unknown : 88",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x88
    Instruction("Unknown : 89",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x89
    Instruction("Unknown : 8A",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x8A
    Instruction("Unknown : 8B",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x8B
    Instruction("Unknown : 8C",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x8C
    Instruction("Unknown : 8D",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x8D
    Instruction("Unknown : 8E",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x8E
    Instruction("Unknown : 8F",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x8F
    Instruction("Unknown : 90",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x90
    Instruction("Unknown : 91",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x91
    Instruction("Unknown : 92",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x92
    Instruction("Unknown : 93",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x93
    Instruction("Unknown : 94",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x94
    Instruction("Unknown : 95",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x95
    Instruction("Unknown : 96",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x96
    Instruction("Unknown : 97",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x97
    Instruction("Unknown : 98",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x98
    Instruction("Unknown : 99",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x99
    Instruction("Unknown : 9A",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x9A
    Instruction("Unknown : 9B",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x9B
    Instruction("Unknown : 9C",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x9C
    Instruction("Unknown : 9D",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x9D
    Instruction("Unknown : 9E",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x9E
    Instruction("Unknown : 9F",        0, 0, pygb.cpu.instructions.misc.nop),   # 0x9F
    Instruction("Unknown : A0",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xA0
    Instruction("Unknown : A1",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xA1
    Instruction("Unknown : A2",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xA2
    Instruction("Unknown : A3",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xA3
    Instruction("Unknown : A4",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xA4
    Instruction("Unknown : A5",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xA5
    Instruction("Unknown : A6",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xA6
    Instruction("Unknown : A7",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xA7
    Instruction("Unknown : A8",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xA8
    Instruction("Unknown : A9",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xA9
    Instruction("Unknown : AA",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xAA
    Instruction("Unknown : AB",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xAB
    Instruction("Unknown : AC",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xAC
    Instruction("Unknown : AD",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xAD
    Instruction("Unknown : AE",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xAE
    Instruction("Unknown : AF",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xAF
    Instruction("Unknown : B0",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xB0
    Instruction("Unknown : B1",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xB1
    Instruction("Unknown : B2",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xB2
    Instruction("Unknown : B3",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xB3
    Instruction("Unknown : B4",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xB4
    Instruction("Unknown : B5",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xB5
    Instruction("Unknown : B6",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xB6
    Instruction("Unknown : B7",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xB7
    Instruction("Unknown : B8",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xB8
    Instruction("Unknown : B9",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xB9
    Instruction("Unknown : BA",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xBA
    Instruction("Unknown : BB",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xBB
    Instruction("Unknown : BC",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xBC
    Instruction("Unknown : BD",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xBD
    Instruction("Unknown : BE",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xBE
    Instruction("Unknown : BF",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xBF
    Instruction("Unknown : C0",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xC0
    Instruction("Unknown : C1",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xC1
    Instruction("Unknown : C2",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xC2
    Instruction("JP 0x%04X",           2, 12, pygb.cpu.instructions.jump.jp_nn),  # 0xC3
    Instruction("Unknown : C4",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xC4
    Instruction("Unknown : C5",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xC5
    Instruction("Unknown : C6",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xC6
    Instruction("Unknown : C7",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xC7
    Instruction("Unknown : C8",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xC8
    Instruction("Unknown : C9",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xC9
    Instruction("Unknown : CA",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xCA
    Instruction("Unknown : CB",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xCB
    Instruction("Unknown : CC",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xCC
    Instruction("Unknown : CD",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xCD
    Instruction("Unknown : CE",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xCE
    Instruction("Unknown : CF",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xCF
    Instruction("Unknown : D0",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xD0
    Instruction("Unknown : D1",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xD1
    Instruction("Unknown : D2",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xD2
    Instruction("Unknown : D3",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xD3
    Instruction("Unknown : D4",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xD4
    Instruction("Unknown : D5",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xD5
    Instruction("Unknown : D6",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xD6
    Instruction("Unknown : D7",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xD7
    Instruction("Unknown : D8",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xD8
    Instruction("Unknown : D9",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xD9
    Instruction("Unknown : DA",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xDA
    Instruction("Unknown : DB",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xDB
    Instruction("Unknown : DC",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xDC
    Instruction("Unknown : DD",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xDD
    Instruction("Unknown : DE",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xDE
    Instruction("Unknown : DF",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xDF
    Instruction("Unknown : E0",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xE0
    Instruction("Unknown : E1",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xE1
    Instruction("Unknown : E2",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xE2
    Instruction("Unknown : E3",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xE3
    Instruction("Unknown : E4",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xE4
    Instruction("Unknown : E5",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xE5
    Instruction("Unknown : E6",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xE6
    Instruction("Unknown : E7",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xE7
    Instruction("Unknown : E8",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xE8
    Instruction("Unknown : E9",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xE9
    Instruction("Unknown : EA",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xEA
    Instruction("Unknown : EB",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xEB
    Instruction("Unknown : EC",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xEC
    Instruction("Unknown : ED",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xED
    Instruction("Unknown : EE",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xEE
    Instruction("Unknown : EF",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xEF
    Instruction("Unknown : F0",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xF0
    Instruction("Unknown : F1",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xF1
    Instruction("Unknown : F2",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xF2
    Instruction("Unknown : F3",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xF3
    Instruction("Unknown : F4",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xF4
    Instruction("Unknown : F5",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xF5
    Instruction("Unknown : F6",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xF6
    Instruction("Unknown : F7",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xF7
    Instruction("Unknown : F8",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xF8
    Instruction("Unknown : F9",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xF9
    Instruction("Unknown : FA",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xFA
    Instruction("Unknown : FB",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xFB
    Instruction("Unknown : FC",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xFC
    Instruction("Unknown : FD",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xFD
    Instruction("Unknown : FE",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xFE
    Instruction("Unknown : FF",        0, 0, pygb.cpu.instructions.misc.nop),   # 0xFF
]