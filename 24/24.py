from operator import add
from enum import StrEnum

class GateOperation(StrEnum):
    AND = "AND"
    OR = "OR"
    XOR = "XOR"

class Gate:
    def __init__(self, input1: str, input2: str, type: GateOperation, output: str):
        self.inputs = (input1, input2)
        self.type = type
        self.output = output
    
    def __repr__(self):
        return f"{self.inputs[0]} {self.type.name} {self.inputs[1]} -> {self.output}"
    
    def get_inputs(self) -> tuple[str]:
        return self.inputs
    
    def get_type(self) -> GateOperation:
        return self.type

    def get_output(self) -> str:
        return self.output
    
class Circuit:
    def __init__(self, fixed_wires: dict, pending_gates: list[Gate]):
        self.fixed_wires = fixed_wires
        self.pending_gates = pending_gates
        self.is_solved = False
    
    def solve(self):
        while len(self.pending_gates) > 0:
            for gate in self.pending_gates:
                input1, input2 = gate.get_inputs()
                if input1 not in self.fixed_wires or input2 not in self.fixed_wires:
                    continue
                output = gate.get_output()
                match gate.get_type():
                    case GateOperation.AND:
                        self.fixed_wires[output] = self.fixed_wires[input1] & self.fixed_wires[input2]
                    case GateOperation.OR:
                        self.fixed_wires[output] = self.fixed_wires[input1] | self.fixed_wires[input2]
                    case GateOperation.XOR:
                        self.fixed_wires[output] = self.fixed_wires[input1] ^ self.fixed_wires[input2]
                self.pending_gates.remove(gate)
        self.is_solved = True
    
    def get_result(self) -> int:
        assert self.is_solved
        z_wires = [wire for wire in self.fixed_wires.keys() if wire[0] == "z"]
        z_wires.sort()
        bits = [self.fixed_wires[wire] for wire in z_wires]
        result = 0
        place_value = 1
        for bit in bits:
            result += bit * place_value
            place_value *= 2
        return result

with open("input.txt", "r") as f:
    lines = f.readlines()

fixed_wires = {}
pending_gates = []
for line in lines:
    if ":" in line:
        tokens = line.split(":")
        fixed_wires[tokens[0]] = int(tokens[1])
    elif "->" in line:
        tokens = line.split()
        pending_gates.append(Gate(tokens[0], tokens[2], GateOperation(tokens[1]), tokens[-1]))

initial_fixed_wires = fixed_wires.copy()
initial_pending_gates = pending_gates.copy()
circuit = Circuit(fixed_wires, pending_gates)
circuit.solve()
result = circuit.get_result()
print(f"Decimal number from z wires: {result}")

def fixed_wires_for_ints(x: int, y: int) -> dict:
    """
    Returns fixed wires for 45-bit unsigned ints
    """
    WORD_LENGTH = 45
    x_bin = bin(x)
    x_bits = [bit for bit in x_bin[2:]]
    if len(x_bits) < WORD_LENGTH:
        x_bits = ["0"] * (WORD_LENGTH - len(x_bits)) + x_bits
    y_bin = bin(y)
    y_bits = [bit for bit in y_bin[2:]]
    if len(y_bits) < WORD_LENGTH:
        y_bits = ["0"] * (WORD_LENGTH - len(y_bits)) + y_bits
    fixed_wires = {f"x{i:02d}": int(b) for i, b in enumerate(x_bits[::-1])}
    fixed_wires.update({f"y{i:02d}": int(b) for i, b in enumerate(y_bits[::-1])})
    return fixed_wires

test_x = [2 ** i for i in range(44)]
test_y = [2 ** i for i in range(44)]
expected = list(map(add, test_x, test_y))
test_count = len(expected)
for i in range(test_count):
    circuit = Circuit(
        fixed_wires_for_ints(test_x[i], test_y[i]),
        initial_pending_gates.copy()
    )
    circuit.solve()
    result = circuit.get_result()
    if result == expected[i]:
        print(f"Passed case {i}: {test_x[i]} + {test_y[i]} = {expected[i]}")
    else:
        print(f"Failed case {i}: expected {test_x[i]} + {test_y[i]} = {expected[i]}, got {result}")

"""
Swaps:
gates with outputs z36 and z37:
wvd XOR rqh -> z36
gng OR qgb -> z37
"""