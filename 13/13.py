from math import gcd, lcm

class Rational:
    def __init__(self, numerator: int, denominator: int):
        g = gcd(numerator, denominator)
        self.numerator = numerator // g
        self.denominator = denominator // g
        if self.numerator < 0 and self.denominator < 0:
            self.numerator = -self.numerator
            self.denominator = -self.denominator

    def get_numerator(self):
        return self.numerator
    
    def get_denominator(self):
        return self.denominator
    
    def add(self, other):
        return Rational(
            other.denominator * self.numerator + self.denominator * other.numerator,
            self.denominator * other.denominator
        )
    
    def sub(self, other):
        return self.add(Rational(-other.numerator, other.denominator))
    
    def mul(self, other):
        return Rational(self.numerator * other.numerator, self.denominator * other.denominator)
    
    def div(self, other):
        if other.numerator == 0:
            raise ZeroDivisionError
        return Rational(self.numerator * other.denominator, self.denominator * other.numerator)
    
    def __eq__(self, other):
        return self.numerator == other.numerator and self.denominator == other.denominator
    
    def __repr__(self):
        return f"{self.numerator} / {self.denominator}"

class ClawMachine:
    a_cost = 3
    b_cost = 1
    max_a_presses = 100
    max_b_presses = 100
    def __init__(self, a_displacement: tuple[int, int], b_displacement: tuple[int, int], prize_location: tuple[int, int]):
        self.a_displacement = a_displacement
        self.b_displacement = b_displacement
        self.prize_location = prize_location

    def __repr__(self):
        return f"ClawMachine with a: {self.a_displacement}, b: {self.b_displacement}, prize at {self.prize_location}"
    
    def rows_are_parallel(self):
        return Rational(b_displacement[0], a_displacement[0]) == Rational(b_displacement[1], a_displacement[1])
    
    def optimal_score(self):
        # -1: infeasible
        if not self.rows_are_parallel():
            numerator = Rational(self.prize_location[1], 1).sub(
                Rational(self.b_displacement[1], self.b_displacement[0]).mul(
                    Rational(self.prize_location[0], 1)
                )
            )
            denominator = Rational(self.a_displacement[1], 1).sub(
                Rational(self.b_displacement[1], self.b_displacement[0]).mul(
                    Rational(self.a_displacement[0], 1)
                )
            )
            a_presses = numerator.div(denominator)
            # if the number of presses isn't a nonnegative integer or is too high, infeasible
            if a_presses.get_denominator() != 1:
                return -1
            if a_presses.get_numerator() > self.max_a_presses or a_presses.get_numerator() < 0:
                return -1
            b_presses = Rational(self.prize_location[0], 1).sub(
                a_presses.mul(Rational(self.a_displacement[0], 1))
            ).div(
                Rational(self.b_displacement[0], 1)
            )
            if b_presses.get_denominator() != 1:
                return -1
            if b_presses.get_numerator() > self.max_b_presses or b_presses.get_numerator() < 0:
                return -1
            return self.a_cost * a_presses.get_numerator() + self.b_cost * b_presses.get_numerator()
        # TODO parallel case
        print(f"Warning: parallel rows for machine {self.__repr__()}! Not counting this score.")
        return -1


with open("input.txt", "r") as f:
    lines = f.readlines()
machines = []
i = 0
while i < len(lines):
    a_button_line = lines[i]
    a_tokens = a_button_line.split()
    a_displacement = (
        int(a_tokens[-2].split("+")[1][:-1]),
        int(a_tokens[-1].split("+")[1]),
    )
    b_button_line = lines[i + 1]
    b_tokens = b_button_line.split()
    b_displacement = (
        int(b_tokens[-2].split("+")[1][:-1]),
        int(b_tokens[-1].split("+")[1]),
    )
    prize_line = lines[i + 2]
    prize_tokens = prize_line.split()
    prize_location = (
        int(prize_tokens[-2].split("=")[1][:-1]),
        int(prize_tokens[-1].split("=")[1]),
    )
    machines.append(ClawMachine(a_displacement, b_displacement, prize_location))
    i += 4

tokens_required = 0
for machine in machines:
    score = machine.optimal_score()
    if score < 0:
        continue
    tokens_required += int(score)
print(f"Fewest tokens, part 1: {tokens_required}")

"""
Part 2
"""
# 64-bit max
ClawMachine.max_a_presses = 18446744073709551615
ClawMachine.max_b_presses = 18446744073709551615
offset = 10000000000000
machines = [
    ClawMachine(m.a_displacement, m.b_displacement, (
        m.prize_location[0] + offset, m.prize_location[1] + offset
    ))
    for m in machines
]
new_tokens_required = 0
for machine in machines:
    score = machine.optimal_score()
    if score < 0:
        continue
    new_tokens_required += int(score)
print(f"Fewest tokens, part 2: {new_tokens_required}")