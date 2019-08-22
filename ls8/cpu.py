"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 25
        self.pc = 0
        self.ir = None
        self.fl = 0b00000000
        self.ops = {
            0b10000010: 'LDI',
            0b01000111: 'PRN',
            0b101000: 'ADD',
            0b10100010: "MUL"
        }

    def load(self, file):
        """Load a program into memory."""

        # convert file into list of binary codes and enter into ram below
        file_lines = open(file, 'r')
        program = file_lines.readlines()

        address = 0

        for instruction in program:
            letter1 = instruction[0]
            if letter1 == '0' or letter1 == '1':
                self.ram_write(address, int(instruction[:8], 2))
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]

        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ir,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        HLT = 0b00000001

        running = True
        while running:
            cmd = self.ram_read(self.pc)
            param1 = self.ram_read(self.pc + 1)
            param2 = self.ram_read(self.pc + 2)

            if cmd == HLT:
                running = False
            elif cmd in self.ops:
                self.ops[cmd](param1, param2)
            else:
                print('Command not found: re-enter')
                running = False

        self.trace()

    def HLT(self):
        exit()

    def LDI(self, param1, param2):
        self.reg[param1] = param2
        self.pc += 3

    def PRN(self, param1):
        print(self.reg[param1])
        self.pc += 2

    def ADD(self, param1, param2):
        self.alu('ADD', param1, param2)
    
    def MUL(self, param1, param2):
        self.alu('MUL', param1, param2)

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr
