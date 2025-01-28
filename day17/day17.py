import re
from enum import Enum
from icecream import ic

class Opcode(Enum):
    ADV = 0
    BXL = 1
    BST = 2
    JNZ = 3
    BXC = 4
    OUT = 5
    BDV = 6
    CDV = 7


class ALU:
    def __init__(self, a: int, b: int, c: int, program: list[int]):
        self.reg_a: int = a
        self.reg_b: int = b
        self.reg_c: int = c
        self.program = program
        self.pc: int = 0
        self._output = []
        self.trace: bool = False

    @property
    def output(self) -> str:
        return ",".join(self._output)

    @property
    def output_len(self) -> int:
        return len(self._output)

    def combo_operand(self, operand: int) -> (int, str):
        if operand < 0:
            raise ValueError('operand must be positive')
        if operand < 4:
            return operand, ""
        if operand == 4:
            return self.reg_a, "A"
        if operand == 5:
            return self.reg_b, "B"
        if operand == 6:
            return self.reg_c, "C"
        raise ValueError('combo operand must be 0 to 6')

    def process(self, opcode: int, operand: int):
        opcode = Opcode(opcode)
        reg = ""
        is_combo = False
        is_mod = False

        if opcode in (Opcode.ADV, Opcode.BST, Opcode.OUT, Opcode.BDV, Opcode.CDV) and operand > 3:
            is_combo = True
        if opcode in (Opcode.BST, Opcode.OUT):
            is_mod = True

        try:
            combo, reg = self.combo_operand(operand)
        except ValueError:
            combo = None

        pc = self.pc
        next_pc = pc + 2
        # ic(a, b, c, pc, opcode, operand, combo)
        left = f"{self.pc:2} {opcode.name}: "
        if opcode == Opcode.ADV:
            self.reg_a = self.reg_a // (2 ** combo)
            if reg:
                left += f"A <- A // 2**{reg} ({2 ** combo})"
            else:
                left += f"A <- A // {2 ** combo}"
        if opcode == Opcode.BXL:
            self.reg_b = self.reg_b ^ operand
            left += f"B <- B XOR {operand}"
        if opcode == Opcode.BST:
            self.reg_b = combo % 8
            if reg:
                left += f"B <- {reg} MOD 8 ({combo})"
            else:
                left += f"B <- {combo} MOD 8"
        if opcode == Opcode.JNZ:
            if self.reg_a:
                next_pc = operand
                left += f"JUMP to {next_pc}"
            else:
                left += f"NO JUMP"
        if opcode == Opcode.BXC:
            self.reg_b = self.reg_b ^ self.reg_c
            left += f"B <- B XOR C"
        if opcode == Opcode.OUT:
            self._output.append(str(combo % 8))
            left += f"OUTPUT -> {self._output[-1]}"
        if opcode == Opcode.BDV:
            self.reg_b = self.reg_a // (2 ** combo)
            if reg:
                left += f"B <- A // 2**{reg} ({2 ** combo})"
            else:
                left += f"B <- A // {2 ** combo}"
        if opcode == Opcode.CDV:
            self.reg_c = self.reg_a // (2 ** combo)
            if reg:
                left += f"C <- A // 2**{reg} ({2 ** combo})"
            else:
                left += f"C <- A // {2 ** combo}"
        self.pc = next_pc
        a = self.reg_a
        b = self.reg_b
        c = self.reg_c
        if self.trace:
            if is_combo:
                trace_operand = f"{reg} ({combo})"
                if is_mod:
                    trace_operand += f" -> {combo%8}"
            else:
                trace_operand = f"{operand}"
            # left = f"{pc}: {opcode.name} {trace_operand}"
            right = f"{a:10o} {b:10o} {c:10o}"
            print(f"{left:32} {right}")


    def run(self):
        while self.pc < len(self.program):
            self.process(self.program[self.pc], self.program[self.pc + 1])

    def dump(self):
        print(f"A={self.reg_a} B={self.reg_b} C={self.reg_c}, pc={self.pc}, output={self.output}")


def tests():
    # ic.enable()
    alu = ALU(a=0, b=0, c=9, program=[2, 6])
    alu.run()
    alu.dump()
    assert alu.reg_b == 1

    alu = ALU(a=10, b=0, c=0, program=[5,0,5,1,5,4])
    alu.run()
    alu.dump()
    assert alu.output == "0,1,2"

    alu = ALU(a=2024, b=0, c=0, program=[0,1,5,4,3,0])
    alu.run()
    alu.dump()
    assert alu.output == "4,2,5,6,7,7,7,7,3,1,0"
    assert alu.reg_a == 0

    alu = ALU(a=0, b=29, c=0, program=[1,7])
    alu.run()
    alu.dump()
    assert alu.reg_b == 26

    alu = ALU(a=0, b=2024, c=43690, program=[4,0])
    alu.run()
    alu.dump()
    assert alu.reg_b == 44354


def main(filename: str):
    register = {}
    with open(filename) as f:
        for line in f:
            if m := re.match(pattern=r"Register ([ABC]): (\d+)", string=line):
                register[m.group(1)] = int(m.group(2))
            if re.match(pattern=r"Program: ", string=line):
                program = [int(x) for x in re.findall(pattern=r"(\d+)", string=line)]

    alu = ALU(register['A'], register['B'], register['C'], program)
    alu.trace = True
    alu.run()
    print(alu.output)

    new_program = program.copy()

    start_value = int("".join([str(x) for x in reversed(new_program)]), base=8)
    start_value *= 6
    print(f"{start_value=}")


    target_output = ",".join([str(x) for x in program])
    alu = ALU(start_value, register['B'], register['C'], program)
    alu.run()
    print(f"   {alu.output=}")
    print(f"{target_output=}")




if __name__ == '__main__':
    ic.lineWrapWidth = 200
    ic.disable()

    # tests()
    # main("sample.txt")
    # main("sample2.txt")
    main("input.txt")