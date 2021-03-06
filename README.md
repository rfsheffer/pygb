PyGB
=============
A GameBoy emulator written in Python

Current Progress
-------
* Memory Space, mapped out, with tests for special echo space
* Load and describe a rom
* A fair number of instructions implemented
* A bare bones graphics tick to get code waiting for VBlank etc working

Current Stage
-------
* Finishing all of the CPU instruction implementations
* Setting up proper instruction timings
* Ensuring the graphics timings are correct
* CPU instruction tests passing

Reasons for creating this project
-------
* To learn how to write a hardware emulator
* Gain a powerful perspective about how things were done in the past
* I appreciate this piece of hardware a lot, and played the hell out of it as a kid
* General Python Practice

Requirements
-------
* Python 3.5+

How to Run
-------
* Clone this repository
* Run python3 main.py --rom "Path to the rom you want to run"

References
-------
* https://cturt.github.io/cinoop.html
* http://www.worldofspectrum.org/faq/reference/z80reference.htm#DAA
* http://www.z80.info
* http://imrannazar.com/GameBoy-Z80-Opcode-Map
* http://gameboy.mongenel.com/dmg/opcodes.html
* http://marc.rawer.de/Gameboy/Docs/GBCPUman.pdf
* http://gbdev.gg8.se/files/roms/blargg-gb-tests/
