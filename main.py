# this is a nonogram japanese puzzle solution using backtracking.
from typing import Tuple

# columns and rows are represented as tuples from left to right and top to bottom to show the input constraints.
# i.e if column1 has 1 2 from top to bottom then they are represented as (1, 2)
columns = [(1,), (2, 1), (1,), (1, 2), (1,)]
rows = [(1,), (1, 2), (1,), (2, 1), (1,)]

def print_state(state):
    for row in state:
        txt = ""
        for col in row:
            txt += str(col) + '\t'
        print(txt)

def print_col(col, state):
    column = [row[col] for row in state]
    print(column)

def backtrack(block_idx, start_idx, current_array, results, block_lengths, total_length):
    if block_idx == len(block_lengths):
        results.append(current_array[:])
        return
    # computes the last valid position so that all blocks fit
    max_start = total_length - sum(block_lengths[block_idx:]) - (len(block_lengths) - block_idx - 1)
    for i in range(start_idx, max_start + 1):
        for j in range(block_lengths[block_idx]):
            current_array[i + j] = 1
        backtrack(block_idx + 1, i + block_lengths[block_idx] + 1, current_array, results, block_lengths, total_length)
        for j in range(block_lengths[block_idx]):
            current_array[i + j] = 0



def my_backtrack(block_idx, start_idx, current_array, results, block_lengths, total_length):
    if block_idx == len(block_lengths):
        results.append(current_array[:])
        return

    max_start = total_length - sum(block_lengths[block_idx:]) - (len(block_lengths) - block_idx - 1) # ????
    # this is total length - remaining block sizes - remaining gaps
    for i in range(start_idx, max_start + 1):
        for j in range(block_lengths[block_idx]):
            current_array[i+j] = 1
        my_backtrack(block_idx+1, i + block_lengths[block_idx] + 1, current_array, results, block_lengths, total_length)
        for j in range(block_lengths[block_idx]):
            current_array[i + j] = 0

def place_blocks(blocks, total_length):
    block_lengths = blocks
    num_blocks = len(block_lengths)
    min_required_length = sum(block_lengths) + (num_blocks - 1)
    if min_required_length > total_length:
        return []

    results = []

    backtrack(0, 0, [0] * total_length, results, block_lengths, total_length)
    return results

def generate_patterns(blocks, total_length):
    return place_blocks(blocks, total_length)

curr_column_states = generate_patterns((1,2), 10)
print(curr_column_states)

def solve_nonogram(state, visited_states):
    pass
# 0 represents white, 1 represents black
# 5x5 example
curr_state = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
]

visited_states = []