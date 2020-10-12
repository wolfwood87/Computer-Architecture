"""CPU functionality."""

import sys

#Standard operations
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111

#Stack operations
POP =  0b01000110
PUSH = 0b01000101

#Set operations
CALL = 0b01010000
RET =  0b00010001
JMP =  0b01010100

#ALU operations
MUL = 0b10100010
ADD = 0b10100000


#Sprint operations
CMP = 0b10100111
JEQ = 0b01010101
JNE = 0b01010110
AND = 0b10101000
NOT = 0b01101001
OR = 0b10101010
XOR = 0b10101011
SHL = 0b10101100
SHR = 0b10101101
MOD = 0b10100100

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.reg[7] = 0xF4
        self.fl = 0b00000000
        self.branchtable = {
            HLT: self.hlt,
            LDI: self.ldi,
            PRN: self.prn,
            POP: self.pop,
            PUSH: self.push
        }
        self.set_table = {
            JMP: self.jump,
            CALL: self.call,
            JEQ: self.jeq,
            JNE: self.jne,
            RET: self.ret
        }
        

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
        #CMP for sprint challenge
        elif op == "CMP":
            if self.reg[reg_a] < self.reg[reg_b]:
                self.fl = 0b00000100
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.fl = 0b00000010
            elif self.reg[reg_a] == self.reg[reg_b]:
                self.fl = 0b00000001
        #sprint challenge
        elif op == "AND":
            self.reg[reg_a] = self.reg[reg_a] & self.reg[reg_b]
        elif op == "OR":
            self.reg[reg_a] = self.reg[reg_a] | self.reg[reg_b]
        elif op == "XOR":
            self.reg[reg_a] = self.reg[reg_a] ^ self.reg[reg_b]
        elif op == "NOT":
            self.reg[reg_a] = ~self.reg[reg_a]
        elif op == "SHL":
            self.reg[reg_a] = self.reg[reg_a] << self.reg[reg_b]
        elif op == "SHR":
            self.reg[reg_a] = self.reg[reg_a] >> self.reg[reg_b]
        elif op == "MOD":
            self.reg[reg_a] = self.reg[reg_a] % self.reg[reg_b]
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
        self.running = True
        while self.running:
            ir = self.ram_read(self.pc)
            num_of_ops = (ir & 0b11111111) >> 6
            alu_indicator = (ir & 0b00100000) >> 5 
            set_indicator = (ir & 0b00010000) >> 4
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            if set_indicator == 1:
                self.set_table[ir](operand_a)
            elif alu_indicator == 1:
                if ir == MUL:
                    self.alu("MUL", operand_a, operand_b)
                    self.pc += 3
                elif ir == ADD:
                    self.alu("ADD", operand_a, operand_b)
                    self.pc += 3
                elif ir == CMP:
                    self.alu("CMP", operand_a, operand_b)
                    self.pc += 3
                elif ir == AND:
                    self.alu("AND", operand_a, operand_b)
                    self.pc += 3
                elif ir == NOT:
                    self.alu("NOT", operand_a)
                    self.pc += 2
                elif ir == OR:
                    self.alu("OR", operand_a, operand_b)
                    self.pc += 3
                elif ir == XOR:
                    self.alu("XOR", operand_a, operand_b)
                    self.pc += 3
                elif ir == SHL:
                    self.alu("SHL", operand_a, operand_b)
                    self.pc += 3
                elif ir == SHR:
                    self.alu("SHR", operand_a, operand_b)
                    self.pc += 3
                elif ir == MOD:
                    self.alu("MOD", operand_a, operand_b)
                else:
                    print("improper ALU operation")
                    self.pc += 3
            else: 
                self.branchtable[ir](operand_a, operand_b)

    def hlt(self, operand_a, operand_b):
        self.running = False

    def ldi(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b
        self.pc += 3

    def prn(self, operand_a, operand_b):
        print(self.reg[operand_a])
        self.pc += 2

    def pop(self, operand_a, operand_b):
        sp = self.reg[7]
        value = self.ram[sp]
        self.reg[operand_a] = value
        if self.reg[7] == 255:
            self.reg[7] = 0
        else:
            self.reg[7] += 1
        self.pc += 2

    def push(self, operand_a, operand_b):
        if self.reg[7] == 0:
            self.reg[7] = 255
        else:
            self.reg[7] -= 1
        value = self.reg[operand_a]
        self.ram[self.reg[7]] = value
        self.pc += 2

    def jump(self, operand_a):
        self.pc = self.reg[operand_a]

    def call(self, operand_a):
        if self.reg[7] == 0:
            self.reg[7] = 255
        else:
            self.reg[7] -= 1
        self.ram[self.reg[7]] = self.pc + 2
        self.pc = self.reg[operand_a]

    def jeq(self, operand_a):
        if self.fl == 0b1:
            self.pc = self.reg[operand_a]
        else:
            self.pc += 2

    def jne(self, operand_a):
        if self.fl != 0b1:
            self.pc = self.reg[operand_a]
        else:
            self.pc += 2

    def ret(self, operand_a):
        value = self.ram[self.reg[7]]
        if self.reg[7] == 255:
            self.reg[7] = 0
        else:
            self.reg[7] += 1
        self.pc = value
# x = CPU()
# x.run()