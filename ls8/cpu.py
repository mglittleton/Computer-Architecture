"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.reg[7] = int('F3', 16)
        self.ram = [0] * 256
        self.PC = 0
        self.IR = None
        self.FL = 0
        self.ops = {
            0b10000010: self.LDI,
            0b01000111: self.PRN,
            0b01000101: self.PUSH,
            0b01000110: self.POP,
            0b10100000: "ADD",
            0b10100010: "MUL",
            0b10100001: "SUB",
            0b10100011: "DIV",
            0b10100100: "MOD",
            0b01010000: self.CALL,
            0b00010001: self.RET,
            0b01010100: self.JMP
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
            self.PC,
            # self.FL,
            # self.IR,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        HLT = 0b00000001

        running = True
        while running:
            cmd = self.ram_read(self.PC)
            param1 = self.ram_read(self.PC + 1)
            param2 = self.ram_read(self.PC + 2)
            num_p = (cmd >> 6)

            if cmd == HLT:
                running = False
            elif bin((cmd >> 5) & 0b00000001) == '0b1':
                self.alu(self.ops[cmd], param1, param2)
                self.PC += num_p + 1
            elif bin((cmd >> 4) & 0b00000001) == '0b1':
                if num_p == 1:
                    self.ops[cmd](param1)
                else: 
                    self.ops[cmd]()
            elif cmd in self.ops:
                if num_p == 2:
                    self.ops[cmd](param1, param2)
                elif num_p == 1:
                    self.ops[cmd](param1)
                else:
                    self.ops[cmd]()
                self.PC += num_p + 1
            else:
                print('Command not found: re-enter')
                running = False

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def LDI(self, reg_loc, val):
        self.reg[reg_loc] = val

    def PRN(self, reg_loc):
        print(self.reg[reg_loc])

    def PUSH(self, reg_loc):
        self.reg[7] = (self.reg[7] - 1) % 255
        SP = self.reg[7]
        val = self.reg[reg_loc]
        self.ram_write(SP, val)

    def POP(self, reg_loc):
        SP = self.reg[7]
        self.reg[7] = (self.reg[7] + 1) % 255
        val = self.ram_read(SP)
        self.reg[reg_loc] = val

    def CALL(self, reg_loc):
        self.reg[7] = (self.reg[7] - 1) % 255
        SP = self.reg[7]
        val = self.PC + 2
        self.PC = self.reg[reg_loc]
        self.ram_write(SP, val)

    def RET(self):
        SP = self.reg[7]
        self.reg[7] = (self.reg[7] + 1) % 255
        self.PC = self.ram_read(SP)

    def JMP(self, reg_loc):
        self.PC = self.reg[reg_loc]


