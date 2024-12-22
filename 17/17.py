class Program:
    def __init__(self, a: int, b: int, c: int, instructions: list[int]):
        self.a = a
        self.b = b
        self.c = c
        self.instruction_pointer = 0
        self.instructions = instructions
        self.output_buffer = []
    
    def execute(self):
        while self.instruction_pointer < len(self.instructions):
            instruction = self.instructions[self.instruction_pointer]
            operand = self.instructions[self.instruction_pointer + 1]
            match instruction:
                case 0:
                    self.adv(operand)
                case 1:
                    self.bxl(operand)
                case 2:
                    self.bst(operand)
                case 3:
                    self.jnz(operand)
                case 4:
                    self.bxc(operand)
                case 5:
                    self.out(operand)
                case 6:
                    self.bdv(operand)
                case 7:
                    self.cdv(operand)
    
    def literal(self, value: int) -> int:
        return value
    
    def combo(self, value: int) -> int:
        match value:
            case 0 | 1 | 2 | 3:
                return value
            case 4:
                return self.a
            case 5:
                return self.b
            case 6:
                return self.c
            case _:
                exit(f"Invalid program: cannot interpret combo value {value}")

    def advance(self):
        self.instruction_pointer += 2

    def adv(self, operand: int):
        self.a = self.a // (2 ** self.combo(operand))
        self.advance()

    def bxl(self, operand: int):
        self.b = self.b ^ self.literal(operand)
        self.advance()

    def bst(self, operand: int):
        self.b = self.combo(operand) % 8
        self.advance()

    def jnz(self, operand: int):
        if self.a == 0:
            self.advance()
            return
        self.instruction_pointer = self.literal(operand)

    def bxc(self, operand: int):
        self.b = self.b ^ self.c
        self.advance()

    def out(self, operand: int):
        self.output_buffer.append(str(self.combo(operand) % 8))
        self.advance()

    def bdv(self, operand: int):
        self.b = self.a // (2 ** self.combo(operand))
        self.advance()

    def cdv(self, operand: int):
        self.c = self.a // (2 ** self.combo(operand))
        self.advance()

    def flush_output(self) -> str:
        string = ",".join(self.output_buffer)
        self.output_buffer.clear()
        return string

with open("input.txt", "r") as f:
    lines = f.readlines()

for line in lines:
    if "Register A:" in line:
        tokens = line.split()
        a = int(tokens[-1])
    elif "Register B:" in line:
        tokens = line.split()
        b = int(tokens[-1])
    elif "Register C:" in line:
        tokens = line.split()
        c = int(tokens[-1])
    elif "Program:" in line:
        tokens = line.split()
        instructions_as_str = tokens[1].split(",")
        instructions = [int(i) for i in instructions_as_str]

program = Program(a, b, c, instructions)
program.execute()
output = program.flush_output()
print(output)

guess = 0
while output != ",".join(instructions_as_str):
    guess += 1
    program = Program(guess, b, c, instructions)
    program.execute()
    output = program.flush_output()
    if guess % 1_000_000 == 0:
        print(f"At guess {guess}")
print(guess)