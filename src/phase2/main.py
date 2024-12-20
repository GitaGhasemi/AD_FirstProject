import time
import tracemalloc

from src.phase2.constants import REFRIGERATION_POINT, BLOCKED_CELL, NEG_INFINITY
from src.phase2.utils import read_inputs, write_outputs


def find_max_happiness_greedy(grid):
    m, n = len(grid), len(grid[0])
    visited_stack = []
    result_stack = []
    path_stack = []
    excluded_neighbors = [set() for _ in range(n)]

    def rollback():
        if result_stack:
            result_stack.pop()
        if path_stack:
            row = path_stack.pop()
            col = len(path_stack)
            excluded_neighbors[col].add(row)
        if visited_stack:
            visited_stack.pop()

    def is_valid_cell(row, col):
        return 0 <= row < m and grid[row][col] != BLOCKED_CELL

    def get_next_start():
        max_value = 0
        selected_row_index = 0
        for row in range(m):
            if row not in excluded_neighbors[0] and grid[row][0] != BLOCKED_CELL and grid[row][0] > max_value:
                max_value = grid[row][0]
                selected_row_index = row
        return selected_row_index

    current_col = 0
    current_row = get_next_start()

    if current_row is None:
        return 0, []

    visited_stack.append((current_row, current_col))
    result_stack.append(grid[current_row][current_col])
    path_stack.append(current_row)

    while current_col < n - 1:
        neighbors = []
        for delta in [-1, 0, 1]:
            neighbor_row = current_row + delta
            if is_valid_cell(neighbor_row, current_col + 1) and neighbor_row not in excluded_neighbors[current_col + 1]:
                value = grid[neighbor_row][current_col + 1]
                if value != BLOCKED_CELL:
                    neighbors.append((value, neighbor_row))

        if not neighbors:
            rollback()
            if not result_stack:
                current_row = get_next_start()
                if current_row is None:
                    return 0, []
                current_col = 0
                visited_stack = [(current_row, current_col)]
                result_stack = [grid[current_row][current_col]]
                path_stack = [current_row]
                excluded_neighbors[0].add(current_row)
                continue
            current_col -= 1
            current_row = path_stack[-1]
            continue

        neighbors.sort(reverse=True, key=lambda x: x[0])
        selected_value, selected_row = neighbors[0]

        if any(grid[row][current_col + 1] == REFRIGERATION_POINT for row in range(m)):
            if grid[selected_row][current_col + 1] != REFRIGERATION_POINT and not any(
                    grid[row][current_col + 1] == REFRIGERATION_POINT for row in path_stack):
                selected_row = next(row for row in range(m) if grid[row][current_col + 1] == REFRIGERATION_POINT)
                selected_value = REFRIGERATION_POINT

        visited_stack.append((selected_row, current_col + 1))
        result_stack.append(selected_value)
        path_stack.append(selected_row)

        current_row = selected_row
        current_col += 1

    return sum(result_stack), [row + 1 for row in path_stack]


def find_max_happiness_dp(grid):
    m, n = len(grid), len(grid[0])
    dp = [[NEG_INFINITY] * n for _ in range(m)]

    for c in range(m):
        dp[c][0] = REFRIGERATION_POINT if grid[c][0] == REFRIGERATION_POINT else grid[c][0]

    for j in range(1, n):
        for i in range(m):
            if grid[i][j] == BLOCKED_CELL:
                dp[i][j] = NEG_INFINITY
                continue

            cell_value = REFRIGERATION_POINT if grid[i][j] == REFRIGERATION_POINT else grid[i][j]
            max_prev = NEG_INFINITY

            if 0 < i < m - 1:
                max_prev = max(
                    dp[i - 1][j - 1] if dp[i - 1][j - 1] != BLOCKED_CELL else NEG_INFINITY,
                    dp[i][j - 1] if dp[i][j - 1] != BLOCKED_CELL else NEG_INFINITY,
                    dp[i + 1][j - 1] if dp[i + 1][j - 1] != BLOCKED_CELL else NEG_INFINITY
                )
            elif i == 0 and i < m - 1:
                max_prev = max(
                    dp[i][j - 1] if dp[i][j - 1] != BLOCKED_CELL else NEG_INFINITY,
                    dp[i + 1][j - 1] if dp[i + 1][j - 1] != BLOCKED_CELL else NEG_INFINITY
                )
            elif i == m - 1:
                max_prev = max(
                    dp[i - 1][j - 1] if dp[i - 1][j - 1] != BLOCKED_CELL else NEG_INFINITY,
                    dp[i][j - 1] if dp[i][j - 1] != BLOCKED_CELL else NEG_INFINITY
                )

            dp[i][j] = cell_value + max_prev if max_prev != NEG_INFINITY else NEG_INFINITY

    max_happiness = max(dp[i][n - 1] for i in range(m))
    path = backtrack_path(dp, grid, n, m)

    return max_happiness, path

def backtrack_path(dp, grid, n, m):
    end_row = -1
    max_val = NEG_INFINITY
    for i in range(m):
        if dp[i][n - 1] > max_val:
            max_val = dp[i][n - 1]
            end_row = i
    path = [0] * n
    path[n - 1] = end_row + 1  # Convert to 1-based index

    for j in range(n - 1, 0, -1):
        current_value = dp[end_row][j]
        cell_value = grid[end_row][j]

        if end_row > 0 and dp[end_row - 1][j - 1] == current_value - cell_value:
            end_row -= 1
        elif end_row < m - 1 and dp[end_row + 1][j - 1] == current_value - cell_value:
            end_row += 1

        path[j - 1] = end_row + 1

    return path

def process_grids(input_file, output_file):
    grids = read_inputs(input_file)
    results = []

    for grid in grids:
        tracemalloc.start()
        start_time = time.time()
        greedy_result, greedy_path = find_max_happiness_greedy(grid)
        greedy_time = time.time() - start_time
        greedy_memory, _ = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        tracemalloc.start()
        start_time = time.time()
        dp_result, dp_path = find_max_happiness_dp(grid)
        dp_time = time.time() - start_time
        dp_memory, _ = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        results.append(
            (grid, greedy_result, greedy_path,
             greedy_time, greedy_memory, dp_result,
             dp_path, dp_time, dp_memory))

    write_outputs(output_file, results)


if __name__ == "__main__":
    input_file = "input/sample_inputs.txt"
    output_file = "output/sample_outputs.txt"

    process_grids(input_file, output_file)
