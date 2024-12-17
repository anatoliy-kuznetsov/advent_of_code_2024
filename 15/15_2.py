class Board:
    width = 100
    height = 50

    def __init__(self, lines: list[str]):
        self.wall_positions = set()
        self.right_box_positions = set()
        self.left_box_positions = set()
        for i, line in enumerate(lines):
            for j, char in enumerate(line[:-1]):
                match char:
                    case "#":
                        self.wall_positions.add((i, 2 * j))
                        self.wall_positions.add((i, 2 * j + 1))
                    case "O":
                        self.left_box_positions.add((i, 2 * j))
                        self.right_box_positions.add((i, 2 * j + 1))
                    case "@":
                        self.robot_position = (i, 2 * j)
                    case _:
                        pass
        
    def __repr__(self):
        board_string = ""
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) in self.wall_positions:
                    board_string += "#"
                elif (i, j) in self.left_box_positions:
                    board_string += "["
                elif (i, j) in self.right_box_positions:
                    board_string += "]"
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
        if all((
            target_position not in self.left_box_positions,
            target_position not in self.right_box_positions,
        )):
            self.robot_position = target_position
            return
        # if moving horizontally, just shift all boxes in the path over by one
        if target_direction[0] == 0:
            current_position = target_position
            while any((
                current_position in self.left_box_positions,
                current_position in self.right_box_positions
            )):
                current_position = (current_position[0] + target_direction[0], current_position[1] + target_direction[1])
            boxes_are_blocked = current_position in self.wall_positions
            if boxes_are_blocked:
                return
            new_left_edges = set()
            new_right_edges = set()
            current_position = target_position
            while any((
                current_position in self.left_box_positions,
                current_position in self.right_box_positions
            )):
                if current_position in self.left_box_positions:
                    new_left_edges.add((current_position[0], current_position[1] + target_direction[1]))
                    self.left_box_positions.remove(current_position)
                else:
                    new_right_edges.add((current_position[0], current_position[1] + target_direction[1]))
                    self.right_box_positions.remove(current_position)
                current_position = (current_position[0], current_position[1] + target_direction[1])
            for edge in new_left_edges:
                self.left_box_positions.add(edge)
            for edge in new_right_edges:
                self.right_box_positions.add(edge)
            self.robot_position = target_position
            return
        
        # if moving vertically, move all clipped boxes
        clipped_boxes = self.find_clipped_boxes(target_position, target_direction[0])
        for box in clipped_boxes:
            box_is_blocked = (box[0] + target_direction[0], box[1]) in self.wall_positions
            if box in self.left_box_positions:
                box_is_blocked = box_is_blocked or (box[0] + target_direction[0], box[1] + 1) in self.wall_positions
            else:
                box_is_blocked = box_is_blocked or (box[0] + target_direction[0], box[1] - 1) in self.wall_positions
            if box_is_blocked:
                return

        new_left_edges = []
        new_right_edges = []
        for box in clipped_boxes:
            if box in self.left_box_positions:
                new_left_edges.append((box[0] + target_direction[0], box[1]))
                self.left_box_positions.remove(box)
            else:
                new_right_edges.append((box[0] + target_direction[0], box[1]))
                self.right_box_positions.remove(box)
        for edge in new_left_edges:
            self.left_box_positions.add(edge)
        for edge in new_right_edges:
            self.right_box_positions.add(edge)
        self.robot_position = target_position

    def find_clipped_boxes(self, root_box_position: tuple[int, int], direction: int) -> set[tuple[int, int]]:
        if not any((
            root_box_position in self.left_box_positions,
            root_box_position in self.right_box_positions
        )):
            return set()
        is_left_edge = root_box_position in self.left_box_positions
        root_box_positions = set([root_box_position])
        search_positions = set([(root_box_position[0] + direction, root_box_position[1])])
        if is_left_edge:
            root_box_positions.add((root_box_position[0], root_box_position[1] + 1))
            search_positions.add((root_box_position[0] + direction, root_box_position[1] + 1))
        else:
            root_box_positions.add((root_box_position[0], root_box_position[1] - 1))
            search_positions.add((root_box_position[0] + direction, root_box_position[1] - 1))
        clipped_box_positions = set()
        for position in search_positions:
            clipped_box_positions = clipped_box_positions.union(
                self.find_clipped_boxes(position, direction)
            )
        return root_box_positions.union(clipped_box_positions)
    
    def sum_gps_coordinates(self):
        gps_coordinate_sum = 0
        for box_position in self.left_box_positions:
            gps_coordinate_sum += 100 * box_position[0] + box_position[1]
        return gps_coordinate_sum

# TODO figure out how to import this from a file named starting with a number
def read_moves(lines: list[str]) -> str:
    horizontal_walls_found = 0
    moves = ""
    for line in lines:
        if "##########" in line:
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
    print(board)
    for i, move in enumerate(moves):
        # print(f"Move {i}: {move}")
        board.apply_move(move)
        # print(board)
    print(f"GPS coordinate sum: {board.sum_gps_coordinates()}")