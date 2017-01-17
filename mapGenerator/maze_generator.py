import random
import numpy

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
def _clear_row(row):
    if not all(isinstance(x, Cell) for x in row):
        raise ValueError("_clear_row: row must be an iterable of Cell class instances")

    for cell in row:
        cell.has_right_border = False
        if cell.has_bottom_border:
            cell.class_num = None
        cell.has_bottom_border = False
    occupied = set([cell.class_num for cell in row if cell.class_num is not None])
    non_occupied = [i for i in range(row) if i not in occupied]

    for cell in row:
        if cell.class_num is None:
            cell.class_num = non_occupied[0]
            del non_occupied[0]
    return row


# Returns list of lists of Cell instances
def generate_Euler(rows_num, cols_num):
    if not (isinstance(rows_num, int) and isinstance(cols_num, int)):
        raise ValueError("MazeGenerator.generate_new: rows_num and cols_num must be int")
    maze = []
    # Initializing the first row
    curr_row = [Cell(i) for i in range(cols_num)]

    # Generating the other but last
    for i in range(rows_num-1):
        if i != 0:
            _clear_row(curr_row)
        _set_right_borders(curr_row)
        _set_bottom_borders(curr_row)
        maze.append(curr_row)

    # Generating the last row
    _clear_row(curr_row)
    for current, next in zip(curr_row, curr_row[1:]):
        current.has_bottom_border = True
        if current.class_num != next.class_num:
            current.has_right_border = False
            next.class_num = current.class_num
    curr_row[-1].has_bottom_border = True
    maze.append(curr_row)

    return maze


def _standard_units_to_cells_num(pass_width, border_width, len_in_standard):
    s = len_in_standard
    b = border_width
    p = pass_width
    return (s-b)//(p+b)


def _cells_num_to_standard_units(len_in_cells, pass_width, border_width):
    n = len_in_cells
    b = border_width
    p = pass_width
    return n*(p+b) + b


def generate_in_standard_units(map_height, map_width, pass_width, border_width):
    if not (isinstance(map_height, int) or (isinstance(map_width, int)) or (isinstance(pass_width, int))
            or (isinstance(border_width, int))):
        raise ValueError("All of the parameters must be int")

    rows = _standard_units_to_cells_num(pass_width, border_width, map_height)
    cols = _standard_units_to_cells_num(pass_width, border_width, map_width)
    maze = generate_Euler(rows, cols)

    result = [[0 for j in range(map_width)] for i in range(map_height)]
    height_std = _cells_num_to_standard_units(len(maze), pass_width, border_width)
    width_std = _standard_units_to_cells_num(len(maze[0]), pass_width, border_width)

    # If height_std < map_height, increase the upmost and bottom-most border width

    # If width_std < map_width, increase the leftmost and rightmost border width
    pass