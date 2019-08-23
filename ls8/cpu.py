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
            0b10000010: self.LDI,
            0b01000111: self.PRN,
            0b10100000: "ADD",
            0b10100010: "MUL",
            0b10100001: "SUB",
            0b10100011: "DIV",
            0b10100100: "MOD",
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
            num_p = 1 + (cmd >> 6)

            if cmd == HLT:
                running = False
            elif bin((cmd >> 5) & 0b00000001) == '0b1':
                self.alu(self.ops[cmd], param1, param2)
                self.pc += num_p
            elif cmd in self.ops:
                self.ops[cmd](param1, param2)
                self.pc += num_p
            else:
                print('Command not found: re-enter')
                running = False

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def LDI(self, param1, param2):
        self.reg[param1] = param2

    def PRN(self, param1, param2):
        print(self.reg[param1])

