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

while len(pending_gates) > 0:
    for gate in pending_gates:
        input1, input2 = gate.get_inputs()
        if input1 not in fixed_wires or input2 not in fixed_wires:
            continue
        output = gate.get_output()
        match gate.get_type():
            case GateOperation.AND:
                fixed_wires[output] = fixed_wires[input1] & fixed_wires[input2]
            case GateOperation.OR:
                fixed_wires[output] = fixed_wires[input1] | fixed_wires[input2]
            case GateOperation.XOR:
                fixed_wires[output] = fixed_wires[input1] ^ fixed_wires[input2]
        pending_gates.remove(gate)

z_wires = [wire for wire in fixed_wires.keys() if wire[0] == "z"]
z_wires.sort()
bits = [fixed_wires[wire] for wire in z_wires]
result = 0
place_value = 1
for bit in bits:
    result += bit * place_value
    place_value *= 2
print(f"Decimal number from z wires: {result}")