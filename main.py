# this is a nonogram japanese puzzle solution using backtracking.
import copy
from itertools import cycle

def print_state(state):
    for row in state:
        txt = ""
        for col in row:
            txt += str(col) + '\t'
        print(txt)

def print_col(col, state):
    column = [row[col] for row in state]
    print(column)

def backtrack(block_idx, start_idx, current_array, block_lengths, total_length):
    if block_idx == len(block_lengths):
        yield current_array[:]
        return
    # computes the last valid position so that all blocks fit
    max_start = total_length - sum(block_lengths[block_idx:]) - (len(block_lengths) - block_idx - 1)
    for i in range(start_idx, max_start + 1):
        for j in range(block_lengths[block_idx]):
            current_array[i + j] = 1
        yield from backtrack(block_idx + 1, i + block_lengths[block_idx] + 1, current_array, block_lengths, total_length)
        for j in range(block_lengths[block_idx]):
            current_array[i + j] = 0

def place_blocks(blocks, total_length):
    block_lengths = blocks
    num_blocks = len(block_lengths)
    min_required_length = sum(block_lengths) + (num_blocks - 1)
    if min_required_length > total_length:
        return []

    yield from backtrack(0, 0, [0] * total_length, block_lengths, total_length)


def generate_patterns(blocks, total_length):
    return place_blocks(blocks, total_length)

curr_column_states = generate_patterns((1,2), 10)
print(curr_column_states)

def solve_nonogram(state, visited_states, cols, rows):
    col_generators = []
    total_length = len(cols)
    for curr_col_vals in cols:
        curr_generator = cycle(generate_patterns(curr_col_vals, total_length))
        col_generators.append(curr_generator)

    return solve(state, visited_states, 0, col_generators, rows, 0)

def solve(state, visited_states, curr_col, col_generators, rows, num_trys_for_first_col):
    if ((curr_col == len(col_generators)) and (not rows_violated(state, rows))) \
            or curr_col > len(col_generators):
        return state, visited_states

    if num_trys_for_first_col > len(rows):
        return [], visited_states

    if curr_col == 0:
        num_trys_for_first_col += 1

    prev_state = copy.deepcopy(state)
    new_col_vals = next(col_generators[curr_col])
    for i in range(len(rows)):
        state[i][curr_col] = new_col_vals[i]

    if state in visited_states:
        for i in range(len(rows)):
            prev_state[i][curr_col] = 0
        return solve(prev_state, visited_states, curr_col-1, col_generators, rows, num_trys_for_first_col)

    if not rows_violated(state, rows):
        return solve(state, visited_states, curr_col+1, col_generators, rows, num_trys_for_first_col)
    else:
        visited_states.append(state)
        return solve(prev_state, visited_states, curr_col, col_generators, rows, num_trys_for_first_col)


def rows_violated(state, rows):
    for i, curr_row in enumerate(state):
        curr_row_conditions = rows[i]
        if sum(curr_row) > sum(curr_row_conditions):
            return True

        start_idx = 0
        for j in curr_row_conditions:
            total_sum = 0
            for k in range(start_idx, len(curr_row)-1):
                total_sum += curr_row[k]
                if total_sum == j:
                    if curr_row[k+1] != 0:
                        return True
                    start_idx = k+1
                    break

    return False


# 0 represents white, 1 represents black
# 5x5 example
curr_state = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

]
# print_state(curr_state)

visited_states = []
# columns and rows are represented as tuples from left to right and top to bottom to show the input constraints.
# i.e if column1 has 1 2 from top to bottom then they are represented as (1, 2)
columns = [(8,), (13,), (2, 7), (2, 9), (7, 6), (8, 5), (7, 5), (4, 1, 6), (14,), (14,), (15,), (4, 2, 5), (5, 6),
           (3, 3), (6,)]
rows = [(7,), (12,), (14,), (1, 11), (1, 3, 3, 1, 1), (1, 9, 1), (1, 4, 4, 2), (2, 3, 3, 2), (4, 3, 1), (5, 4, 1),
        (13,), (13,), (13,), (13,), (8, 3)]

solved_state, visited_states = solve_nonogram(curr_state, visited_states, columns, rows)
print_state(solved_state)
# patterns = cycle(generate_patterns((1, 3, 3, 1, 1), 15))
# for i in range(15):
#     next_pattern = next(patterns)
#     print(next_pattern)
# rows_violated(curr_state, rows)
