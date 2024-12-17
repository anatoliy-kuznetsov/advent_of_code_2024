class Board:
    width = 50
    height = 50

    def __init__(self, lines: list[str]):
        self.wall_positions = set()
        self.box_positions = set()
        for i, line in enumerate(lines):
            for j, char in enumerate(line[:-1]):
                match char:
                    case "#":
                        self.wall_positions.add((i, j))
                    case "O":
                        self.box_positions.add((i, j))
                    case "@":
                        self.robot_position = (i, j)
                    case _:
                        pass
        
    def __repr__(self):
        board_string = ""
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) in self.wall_positions:
                    board_string += "#"
                elif (i, j) in self.box_positions:
                    board_string += "O"
                elif (i, j) == self.robot_position:
                    board_string += "@"
                else:
                    board_string += "."
            board_string += "\n"
        return board_string
    
    def apply_move(self, move: str):
        assert len(move) == 1
        match move:
            case "^":
                target_direction = (-1, 0)
            case ">":
                target_direction = (0, 1)
            case "v":
                target_direction = (1, 0)
            case "<":
                target_direction = (0, -1)
            case _:
                raise ValueError(f"Invalid move '{move}'")
        target_position = (self.robot_position[0] + target_direction[0], self.robot_position[1] + target_direction[1])
        if target_position in self.wall_positions:
            return
        if target_position not in self.box_positions:
            self.robot_position = target_position
            return
        current_position = target_position
        while current_position in self.box_positions:
            current_position = (current_position[0] + target_direction[0], current_position[1] + target_direction[1])
        boxes_are_blocked = current_position in self.wall_positions
        if boxes_are_blocked:
            return
        # to model the motion of the stack of boxes, we can just push one onto the end and pop the first
        self.box_positions.add(current_position)
        self.box_positions.remove(target_position)
        self.robot_position = target_position
    
    def sum_gps_coordinates(self):
        gps_coordinate_sum = 0
        for box_position in self.box_positions:
            gps_coordinate_sum += 100 * box_position[0] + box_position[1]
        return gps_coordinate_sum

def read_moves(lines: list[str]) -> str:
    horizontal_walls_found = 0
    moves = ""
    for line in lines:
        if "##################################################" in line:
            horizontal_walls_found += 1
            continue
        if horizontal_walls_found < 2:
            continue
        line_moves = line[:-1]
        moves += line_moves
    return moves

if __name__ == "__main__":
    with open("input.txt", "r") as f:
        lines = f.readlines()

    board = Board(lines)
    moves = read_moves(lines)
    for move in moves:
        board.apply_move(move)
    print(f"GPS coordinate sum: {board.sum_gps_coordinates()}")