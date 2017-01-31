import random
import numpy as np
from copy import deepcopy


class Cell:
    class_num = None
    has_right_border = False
    has_bottom_border = False

    def __init__(self, class_num):
        self.class_num = class_num


def _set_right_borders(row):
    if not all(isinstance(x, Cell) for x in row):
        raise ValueError("_set_right_borders: row must be an iterable of Cell class instances")

    for current, next in zip(row, row[1:]):
        if current.class_num == next.class_num:
            current.has_right_border = True
        do_set = random.randint(0, 1)
        if do_set:
            current.has_right_border = True
        else:
            next.class_num = current.class_num
    return row


def _set_bottom_borders(row):
    if not all(isinstance(x, Cell) for x in row):
        raise ValueError("_set_bottom_borders: row must be an iterable of Cell class instances")

    ''' Check, if at least one Cell of this class_num does not have bottom border '''
    has_any_without = set()

    for cell in row:
        if cell.class_num not in has_any_without:
            cell.has_bottom_border = False
            has_any_without.add(cell.class_num)
            continue
        do_set = random.randint(0, 1)
        if do_set:
            cell.has_bottom_border = True
        else:
            cell.has_bottom_border = False

    return row


# Deleting the right borders and producing some operations with the bottom ones
def _copy_and_clear_row(row):
    if not all(isinstance(x, Cell) for x in row):
        raise ValueError("_clear_row: row must be an iterable of Cell class instances")
    result = deepcopy(row)
    for cell in result:
        cell.has_right_border = False
        if cell.has_bottom_border:
            cell.class_num = None
        cell.has_bottom_border = False
    occupied = set([cell.class_num for cell in result if cell.class_num is not None])
    non_occupied = [i for i in range(len(result)) if i not in occupied]

    for cell in result:
        if cell.class_num is None:
            cell.class_num = non_occupied[0]
            del non_occupied[0]
    return result


def _print_row(row):
    print("|", end="")
    for cell in row:
        if cell.has_bottom_border:
            print("_", end="")
        else:
            print(" ", end="")
        if cell.has_right_border:
            print("|", end="")
        else:
            print(" ", end="")
    print("|")


# Returns list of lists of Cell instances
def _generate_Euler(rows_num, cols_num):
    if not (isinstance(rows_num, int) and isinstance(cols_num, int)):
        raise ValueError("MazeGenerator.generate_new: rows_num and cols_num must be int")
    maze = []
    # Initializing the first row
    curr_row = [Cell(i) for i in range(cols_num)]

    # Generating all rows but last
    for i in range(rows_num):
        if i != 0:
            curr_row = _copy_and_clear_row(curr_row)
        curr_row = _set_right_borders(curr_row)
        curr_row = _set_bottom_borders(curr_row)
        maze.append(curr_row[:])

    return maze


def _standard_units_to_cells_num(pass_width, border_width, len_in_standard):
    s = len_in_standard
    b = border_width
    p = pass_width
    return (s - b) // (p + b)


def _cells_num_to_standard_units(len_in_cells, pass_width, border_width):
    n = len_in_cells
    b = border_width
    p = pass_width
    return n * (p + b) + b


def _print_raw(maze):
    for row in maze:
        _print_row(row)


def generate_in_standard_units(map_width, map_height, pass_width, border_width, filename_out=None):
    if not (isinstance(map_height, int) or (isinstance(map_width, int)) or (isinstance(pass_width, int))
            or (isinstance(border_width, int))):
        raise ValueError("All of the parameters must be int")

    rows = _standard_units_to_cells_num(pass_width, border_width, map_height)
    cols = _standard_units_to_cells_num(pass_width, border_width, map_width)
    maze = _generate_Euler(rows, cols)
    # TEST
    _print_raw(maze)

    result = np.zeros((map_height, map_width), dtype=int)
    height_std = _cells_num_to_standard_units(len(maze), pass_width, border_width)
    width_std = _cells_num_to_standard_units(len(maze[0]), pass_width, border_width)

    d_top, d_bottom, d_left, d_right = 0, 0, 0, 0

    # If height_std < map_height, increase the upmost and bottom-most border width
    tmp = (map_height - height_std) // 2
    d_top += tmp
    d_bottom += (map_height - height_std) - tmp
    # If width_std < map_width, increase the leftmost and rightmost border width
    tmp = (map_width - width_std) // 2
    d_left += tmp
    d_right += (map_width - width_std) - tmp
    # Lately we'll draw only right and bottom borders
    d_top += border_width
    d_left += border_width

    #  We draw only right and bottom borders
    top_i = d_top  # index of the top of the cell
    p = pass_width
    b = border_width
    for row in maze:
        left_i = d_left  # index of the left side of the cell
        for cell in row:
            if cell.has_right_border:
                result[top_i : (top_i + p + b), left_i + p : (left_i + p) + b] = 1
            if cell.has_bottom_border:
                result[top_i + p : (top_i + p) + b, left_i: (left_i + p + b)] = 1
            left_i += p + b
        top_i += p + b

    # Saving to the file
    if filename_out is not None:
        with open(filename_out, 'w') as f:
            f.write(str(map_width) + " " + str(map_height) + "\n")
            for row in result:
                for i in row:
                    f.write(str(i) + " ")
                f.write("\n")
    return result
