"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b00000010
PRN = 0b00000111

#Stack operations
POP =  0b00000110
PUSH = 0b00000101

#ALU operations
MUL = 0b10100010
ADD = 0b10100000

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.reg[7] = 0xF4

    def load(self, filename):
        """Load a program into memory."""
        address = 0
        # if len(sys.argv) == 2:
        #     filename = sys.argv[1]
        # else:
        #     print("please pass a file name as an argument")
        #     sys.exit()
        
        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1
        try:
            with open(filename, "r") as f:
                for line in f:
                    possible_number = line[:line.find("#")]
                    if possible_number == "":
                        continue
                    instruction = int(possible_number, 2)
                    self.ram[address] = instruction
                    address += 1
        
        except FileNotFoundError:
            print(f"We did not find file {filename}")

    def ram_read(self, mar):
        return self.ram[mar]
    
    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
# F3 start of stack
    def run(self):
        # self.load()
        running = True
        while running:
            ir = self.ram_read(self.pc)
            num_of_ops = (ir & 0b11111111) >> 6
            alu_indicator = (ir & 0b00100000) >> 5 
            set_indicator = (ir & 0b00010000) >> 4
            instructions = ir & 0b00001111
            if num_of_ops >= 1:
                operand_a = self.ram_read(self.pc + 1)
            if num_of_ops == 2:
                operand_b = self.ram_read(self.pc + 2)
            if alu_indicator == 1:
                if ir == MUL:
                    self.alu("MUL", operand_a, operand_b)
                    self.pc += 3
                elif ir == ADD:
                    self.alu("ADD", operand_a, operand_b)
                    self.pc += 3
                else:
                    print("improper ALU operation")
                    self.pc += 3
            elif instructions == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif instructions == PUSH:
                if self.reg[7] == 0:
                    self.reg[7] = 255
                else:
                    self.reg[7] -= 1
                value = self.reg[operand_a]
                self.ram[self.reg[7]] = value
                self.pc += 2
            elif instructions == POP:
                sp = self.reg[7]
                value = self.ram[sp]
                self.reg[operand_a] = value
                if self.reg[7] == 255:
                    self.reg[7] = 0
                else:
                    self.reg[7] += 1
                self.pc += 2
            elif instructions == PRN:
                print(self.reg[operand_a])
                self.pc += 2
            elif instructions == HLT:
                print("end of program")
                running = False
                exit()
            else:
                print("unknown command")
                running = False


# x = CPU()
# x.run()