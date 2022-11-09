import numpy as np
# this file contains solving functions, plus the board validation function


def get_invalid_nums_pos(puzzle):  # get numbers, that are duplicates, and highlight them with red color, to tell the user that this placement in invalid and creates already impossible sudoku
    invalid_nums_pos = set()

    puzzle_copy = puzzle.copy()

    # so we need to find duplicates in each row, column and 3x3 grids (faster -> better) which this function, conveniently does



    # --------------------ITERATE--OVER--ROWS-------------------------

    # first we iterate over each row to find duplicates
    for row_counter, row in enumerate(puzzle_copy):
        duplicates = get_duplicates(np.concatenate(row))

        for duplicate_n in duplicates:  # we know duplicate numbers, now we need to spot their position
            if duplicate_n != 0:  # if the duplicate number is 0, then there is no need to highlight it, since empty cells duplicates are allowed. duh
                for line_counter, line in enumerate(row):
                    for cell_counter, cell_value in enumerate(line):
                        if cell_value == duplicate_n:
                            cell_pos = ({(row_counter, line_counter, cell_counter)})  # cell pos has 3 values, since we need to know the row index, the line index and the element index inside tha line
                            invalid_nums_pos.update(cell_pos)



    # --------------------ITERATE--OVER--COLUMNS-------------------------

    # second, we iterate over each column to find duplicates
    puzzle_copy = [[] for _ in range(9)]
    for row_counter, row in enumerate(puzzle):
        puzzle_copy[row_counter] = np.concatenate(row)  # waring here that i cant fix

    puzzle_copy = np.array(puzzle_copy)

    for column_counter, column in enumerate(puzzle_copy.transpose()):
        # so because of the way the 'puzzle' list is structured, the transpose() function iterates in a very weird way. It goes over every first element in the lines in a row, then over the second element, and then the third. So the way I ahd to solve it changed a little bit the math i had to make. So the math here may feel confusing. But hey, you don't need to understand the math really
        duplicates = get_duplicates(column)

        for duplicate_n in duplicates:  # we know duplicate numbers, now we need to spot their position
            if duplicate_n != 0:  # if the duplicate number is 0, then there is no need to highlight it, since empty cells duplicates are allowed. duh
                for cell_counter, cell_value in enumerate(column):
                    if cell_value == duplicate_n:
                        cell_pos = ({(cell_counter, column_counter // 3, column_counter % 3)})  # cell pos has 3 values, since we need to know the row index, the line index and the element index inside tha line
                        invalid_nums_pos.update(cell_pos)



    # --------------------ITERATE--OVER--GRIDS-------------------------

    # last check we need to make. Now we iterate over every grid in the puzzle, and check if it contains any duplicates (check sudoku rules, i don't really need to explain this)
    puzzle_copy = convert_puzzle_to_another_type(puzzle, "to grid")

    for grid_counter, grid in enumerate(puzzle_copy):
        duplicates = get_duplicates(np.concatenate(grid))

        for duplicate_n in duplicates:
            if duplicate_n != 0:
                for grid_row_counter, grid_row in enumerate(grid):
                    for cell_counter, cell_value in enumerate(grid_row):
                        if cell_value == duplicate_n:
                            cell_pos = ({(grid_row_counter + (grid_counter//3)*3, grid_counter % 3, cell_counter)})
                            invalid_nums_pos.update(cell_pos)

    return list(invalid_nums_pos)


def get_hints_positions(puzzle):
    hints_pos = []  # will contain tuples, with indexes indicating that this cell is a hint

    for row_counter, row in enumerate(puzzle):
        for line_counter, line in enumerate(row):
            for cell_counter, cell_value in enumerate(line):
                # remember, 0 is an indicator, that this is an empty cell
                if cell_value != 0:  # you can understand this bruh (why "bruh" is highlighted? its a real word)
                    cell_pos = (row_counter, line_counter, cell_counter)

                    hints_pos.append(cell_pos)

    return hints_pos  # :/


def get_duplicates(array):
    sorted_array = np.sort(array, axis=None)
    return list(set(sorted_array[:-1][sorted_array[1:] == sorted_array[:-1]]))  # some crazy duplication glitch patch that i barely understand


def remove_overlapping_values(candidate_list, puzzle):
    """
    NO CANDIDATES MUST OVERLAP WITH PUZZLE HINTS OR GUESSES

    :param candidate_list: ...
    :param puzzle: the puzzle itself. Bro, its not that hard to realize
    :return: the IMPROVED and FIXED candidate_pos list
    """

    for row_counter, row in enumerate(puzzle):
        for line_counter, line in enumerate(row):
            for cell_counter, cell_value in enumerate(line):
                if cell_value != 0:
                    candidate_list[row_counter][line_counter * 3 + cell_counter] = []

    return candidate_list


def convert_puzzle_to_another_type(puzzle, t):  # t - type, which type to convert into. This function is used to convert puzzle into two different types: the row-based type and grid-based type. Row-based type is a list of rows, where each element is a row. Grid-based type is a list of grids, where each element is a 3x3 grid of the puzzle. its used for special cases, where using that type is much easier
    # every the time we use this function, we know the type of the puzzle list, so we just specify another type in "t" attribute
    new_puzzle = [[] for _ in range(9)]

    if t == "to grid":  # convert to grid type
        for row_counter, row in enumerate(puzzle):
            grids_row_index = row_counter // 3
            # basically, its a variable that indicates which 3 of 9 grids are gonna be used. First 3, second 3 or last 3
            # also you can call it a "y" coordinate of grids that we use

            for line_counter, line in enumerate(row):
                new_puzzle[line_counter + grids_row_index * 3].append(line.tolist())
                # so the math works like this: line counter indicates which grid we use, basically a "x" coordinate, and grids_row_index is a "y" coordinate. we multiply it by 3, because, lets say, we take the middle grid in the center, and take both x and y coordinates. If we just sum them we will get 2 (cuz middle, x = 1, y = 1) which is definitely not the index of that thing. But if we multiply the second one by 3, we get 1+ 3 = 4 which is the index of the grid in the list

    if t == "to row":  # convert to row type
        for grid_counter, grid in enumerate(puzzle):
            for grid_row_counter, grid_row in enumerate(grid):
                row_index = grid_row_counter + (grid_counter // 3) * 3

                new_puzzle[row_index].append(grid_row.tolist())

    return np.array(new_puzzle)


def check_sudoku_solved(puzzle):
    for row in puzzle:
        for line in row:
            for cell in line:
                if cell == 0:
                    return False

    return True
