from collections import defaultdict

class Region:
    def __init__(self, indices: tuple[int, int], letter: str):
        self.cells = [indices]
        self.letter = letter

    def merge(self, other):
        """
        Copies other cells into these ones.
        Other can then be safely destroyed.
        """
        self.cells.extend(other.cells)

    def add(self, indices: tuple[int, int]):
        self.cells.append(indices)

    def abuts(self, indices: tuple[int, int]) -> bool:
        i = indices[0]
        j = indices[1]
        for (existing_i, existing_j) in self.cells:
            if abs(existing_i - i) + abs(existing_j - j) == 1:
                return True
        return False

    def area(self) -> int:
        return len(self.cells)
    
    def perimeter(self) -> int:
        adjacent_pair_count = 0
        for index1 in range(len(self.cells)):
            for index2 in range(index1, len(self.cells)):
                i1, j1 = self.cells[index1]
                i2, j2 = self.cells[index2]
                if abs(i1 - i2) + abs(j1 - j2) == 1:
                    adjacent_pair_count += 1
        return 4 * len(self.cells) - 2 * adjacent_pair_count
    
    def horizontal_sides(self) -> dict:
        # key: row index below horizontal side. values: column indices participating in side
        horizontal_side_segments = defaultdict(lambda: [])
        for cell in self.cells:
            # above the cell
            cell_exists_above = (cell[0] - 1, cell[1]) in self.cells
            if cell_exists_above:
                # remove old segment
                for segment in horizontal_side_segments[cell[0]]:
                    if cell[1] in segment:
                        segment.remove(cell[1])
                        break
            else:
                matching_horizontal_segments_above = []
                for segment in horizontal_side_segments[cell[0]]:
                    for other_column_index in segment:
                        if other_column_index == cell[1] - 1 and (cell[0], cell[1] - 1) in self.cells:
                            matching_horizontal_segments_above.append(segment)
                        elif other_column_index == cell[1] + 1 and (cell[0], cell[1] + 1) in self.cells:
                            matching_horizontal_segments_above.append(segment)
                if len(matching_horizontal_segments_above) == 0:
                    horizontal_side_segments[cell[0]].append([cell[1]])
                else:
                    for segment in matching_horizontal_segments_above[1:]:
                        matching_horizontal_segments_above[0].extend(segment)
                        horizontal_side_segments[cell[0]].remove(segment)
                    matching_horizontal_segments_above[0].append(cell[1])
            # below the cell
            cell_exists_below = (cell[0] + 1, cell[1]) in self.cells
            if cell_exists_below:
                # remove old segment
                for segment in horizontal_side_segments[cell[0] + 1]:
                    if cell[1] in segment:
                        segment.remove(cell[1])
                        break
            else:
                matching_horizontal_segments_below = []
                for segment in horizontal_side_segments[cell[0] + 1]:
                    for other_column_index in segment:
                        if other_column_index == cell[1] - 1 and (cell[0], cell[1] - 1) in self.cells:
                            matching_horizontal_segments_below.append(segment)
                        elif other_column_index == cell[1] + 1 and (cell[0], cell[1] + 1) in self.cells:
                            matching_horizontal_segments_below.append(segment)
                if len(matching_horizontal_segments_below) == 0:
                    horizontal_side_segments[cell[0] + 1].append([cell[1]])
                else:
                    for segment in matching_horizontal_segments_below[1:]:
                        matching_horizontal_segments_below[0].extend(segment)
                        horizontal_side_segments[cell[0] + 1].remove(segment)
                    matching_horizontal_segments_below[0].append(cell[1])
        return {index: segment for (index, segment) in horizontal_side_segments.items() if len(segment) > 0}
    
    def vertical_sides(self) -> dict:
        # key: column index to the right of vertical side. values: row indices participating in side
        vertical_side_segments = defaultdict(lambda: [])
        for cell in self.cells:
            # left of the cell
            cell_exists_left = (cell[0], cell[1] - 1) in self.cells
            if cell_exists_left:
                # remove old segment
                for segment in vertical_side_segments[cell[1]]:
                    if cell[0] in segment:
                        segment.remove(cell[0])
                        break
            else:
                matching_vertical_segments_left = []
                for segment in vertical_side_segments[cell[1]]:
                    for other_row_index in segment:
                        if other_row_index == cell[0] - 1 and (cell[0] - 1, cell[1]) in self.cells:
                            matching_vertical_segments_left.append(segment)
                        elif other_row_index == cell[0] + 1 and (cell[0] + 1, cell[1]) in self.cells:
                            matching_vertical_segments_left.append(segment)
                if len(matching_vertical_segments_left) == 0:
                    vertical_side_segments[cell[1]].append([cell[0]])
                else:
                    for segment in matching_vertical_segments_left[1:]:
                        matching_vertical_segments_left[0].extend(segment)
                        vertical_side_segments[cell[1]].remove(segment)
                    matching_vertical_segments_left[0].append(cell[0])
            # right of the cell
            cell_exists_right = (cell[0], cell[1] + 1) in self.cells
            if cell_exists_right:
                # remove old segment
                for segment in vertical_side_segments[cell[1] + 1]:
                    if cell[0] in segment:
                        segment.remove(cell[0])
                        break
            else:
                matching_vertical_segments_right = []
                for segment in vertical_side_segments[cell[1] + 1]:
                    for other_row_index in segment:
                        if other_row_index == cell[0] - 1 and (cell[0] - 1, cell[1]) in self.cells:
                            matching_vertical_segments_right.append(segment)
                        elif other_row_index == cell[0] + 1 and (cell[0] + 1, cell[1]) in self.cells:
                            matching_vertical_segments_right.append(segment)
                if len(matching_vertical_segments_right) == 0:
                    vertical_side_segments[cell[1] + 1].append([cell[0]])
                else:
                    for segment in matching_vertical_segments_right[1:]:
                        matching_vertical_segments_right[0].extend(segment)
                        vertical_side_segments[cell[1] + 1].remove(segment)
                    matching_vertical_segments_right[0].append(cell[0])

        return {index: segment for (index, segment) in vertical_side_segments.items() if len(segment) > 0}
    
    def count_sides(self) -> int:
        horizontal_side_count = sum(len(row_sides) for row_sides in self.horizontal_sides().values())
        vertical_side_count = sum(len(column_sides) for column_sides in self.vertical_sides().values())
        return horizontal_side_count + vertical_side_count

    def price_perimeter(self) -> int:
        return self.area() * self.perimeter()
    
    def price_sides(self) -> int:
        return self.area() * self.count_sides()
    
    def __repr__(self):
        return f"Region of letter {self.letter} with cells {self.cells}\n" \
                f"\t{sum(len(row_sides) for row_sides in self.horizontal_sides().values())} horizontal sides {self.horizontal_sides()}\n" \
                f"\t{sum(len(column_sides) for column_sides in self.vertical_sides().values())} vertical sides {self.vertical_sides()}"
    
with open("input.txt", "r") as f:
    lines = f.readlines()

# trim newline characters
farm_map = [line[:-1] for line in lines]
# collection of regions. key: letter, value: list of regions with that letter
regions = defaultdict(lambda: [])
for i in range(len(farm_map)):
    for j in range(len(farm_map[0])):
        letter = farm_map[i][j]
        adjacent_regions_found = []
        for matching_region in regions[letter]:
            if matching_region.abuts((i, j)):
                adjacent_regions_found.append(matching_region)
        if len(adjacent_regions_found) == 0:
            regions[letter].append(Region(indices=(i, j), letter=letter))
        else:
            for additional_region in adjacent_regions_found[1:]:
                adjacent_regions_found[0].merge(additional_region)
                regions[letter].remove(additional_region)
            adjacent_regions_found[0].add((i, j))

print(f"Total price using perimeter: {sum(sum(region.price_perimeter() for region in letter_regions) for letter_regions in regions.values())}")
print(f"Total price using sides: {sum(sum(region.price_sides() for region in letter_regions) for letter_regions in regions.values())}")