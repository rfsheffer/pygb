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


from pygb.cpu import registers
from pygb.memory.memory import MemoryPool
from pygb.cpu.instructions.instructions import instructions

from pygb.settings import DEBUG
from pygb.cpu.instructions.misc import nop

class Capabilities:
    cpu_clock_mhz = 4.194304


class CPU:
    def __init__(self, memory_space):
        self.registers = registers.RegisterBank()
        self.memory = memory_space  # type: MemoryPool

    def reset(self):
        # Setup the registers
        self.registers.set_a(0x01)
        self.registers.set_f(0xB0)
        self.registers.set_b(0x00)
        self.registers.set_c(0x13)
        self.registers.set_d(0x00)
        self.registers.set_e(0xD8)
        self.registers.set_h(0x01)
        self.registers.set_l(0x4D)
        self.registers.set_sp(0xFFFE)

        # On power up, the GameBoy Program Counter is initialized to 0x100
        self.registers.set_pc(0x0100)

    def step(self):
        cur_pc = self.registers.get_pc()
        self.registers.inc_pc()
        op_code = self.memory.read_byte(cur_pc)
        if len(instructions) <= op_code:
            raise Exception('Instruction op-code was beyond our op-code range!')

        instruction = instructions[op_code]
        if op_code != 0x00 and instruction.execute is nop:
            raise(Exception('Unhandled op code 0x%02X!' % op_code))

        if DEBUG:
            operand = 0
            if instruction.operand_len == 1:
                operand = self.memory.read_byte(self.registers.get_pc())
            elif instruction.operand_len == 2:
                operand = self.memory.read_short(self.registers.get_pc())

            print("%02X - " % op_code, end='')
            if instruction.operand_len:
                print(instruction.disassembly % operand)
            else:
                print(instruction.disassembly)

        # Execute the CPU instruction
        instruction.execute(instruction, self.registers, self.memory)

        # Increment the program counter by the operand length (jumping over the operand)
        # We post increment because our instructions read (PC) like any other register
        # and we do not want the PC to be incremented before the instruction or it will dereference
        # to the wrong value. Some instructions change the PC such as JP, so we ignore increment in those cases.
        if not instruction.changes_pc:
            self.registers.inc_pc(instruction.operand_len)

        if DEBUG:
            self.registers.print_registers()
