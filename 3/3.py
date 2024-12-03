import re

mul_pattern = r'mul\([0-9]+,[0-9]+\)'

with open("input.txt", "r") as f:
    program = f.read()

valid_mul_commands = re.findall(mul_pattern, program)

def evaluate_mul_command(command: str) -> int:
    tokens = command.split(",")
    first_multiplicand = int(tokens[0][4:])
    second_multiplicand = int(tokens[1][:-1])
    return first_multiplicand * second_multiplicand

print(f"All mul commands:\t{sum(evaluate_mul_command(command) for command in valid_mul_commands)}")

enabled_mul_pattern = r"(?<=do\(\))[\s\S]*?mul\([0-9]+,[0-9]+\)[\s\S]*?(?=don't\(\))"
first_dont_position = program.find("don't()")
first_commands = re.findall(mul_pattern, program[:first_dont_position])
enabled_result = sum(evaluate_mul_command(command) for command in first_commands)
remaining_command_chunks = re.findall(enabled_mul_pattern, program)
remaining_commands = []
for chunk in remaining_command_chunks:
    remaining_commands.extend(re.findall(mul_pattern, chunk))
enabled_result += sum(evaluate_mul_command(command) for command in remaining_commands)
print(f"Enabled mul commands:\t{enabled_result}")