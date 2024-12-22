import os

from src.interfaces.max_happiness_interface import MaxHappinessInterface
from src.constants import *


class MaxHappinessPhase3(MaxHappinessInterface):
    def __init__(self, input_path=None, output_path=None):
        # Default paths using os library if paths are not passed
        if input_path is None:
            input_path = os.path.join(os.path.dirname(__file__), INPUT_FILE_PATH)
        if output_path is None:
            output_path = os.path.join(os.path.dirname(__file__), OUTPUT_FILE_PATH)

        self._input_path = os.path.abspath(input_path)
        self._output_path = os.path.abspath(output_path)

    @property
    def input_path(self):
        return self._input_path

    @property
    def output_path(self):
        return self._output_path

    def find_max_happiness_greedy(self, grid):
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

        def get_next_start(col):
            """
            Get the row index with the largest value in the specified column.
            If no valid row exists, return None.
            """
            max_value = NEG_INFINITY
            selected_row_index = None
            for row in range(m):
                if row not in excluded_neighbors[col] and grid[row][col] != BLOCKED_CELL:
                    if grid[row][col] > max_value:
                        max_value = grid[row][col]
                        selected_row_index = row
            return selected_row_index

        current_col = 0
        current_row = None

        # Find the first valid starting point
        while current_col < n and current_row is None:
            current_row = get_next_start(current_col)
            if current_row is None:
                current_col += 1

        if current_row is None:  # No valid starting point in the entire grid
            return 0, []

        visited_stack.append((current_row, current_col))
        result_stack.append(grid[current_row][current_col])
        path_stack.append(current_row)

        while current_col < n - 1:
            neighbors = []
            for delta in [-1, 0, 1]:
                neighbor_row = current_row + delta
                if is_valid_cell(neighbor_row, current_col + 1) and\
                        neighbor_row not in excluded_neighbors[current_col + 1]:
                    value = grid[neighbor_row][current_col + 1]
                    if delta == 0:
                        value += 1
                    else:
                        value -= 1
                    neighbors.append((value, neighbor_row))

            if not neighbors:  # No valid neighbors, rollback
                rollback()
                if not result_stack:  # If rollback empties result_stack, find a new starting point
                    current_row = None
                    while current_col < n and current_row is None:
                        current_row = get_next_start(current_col)
                        if current_row is None:
                            current_col += 1
                    if current_row is None:  # No valid starting point
                        return 0, []
                    visited_stack = [(current_row, current_col)]
                    result_stack = [grid[current_row][current_col]]
                    path_stack = [current_row]
                    excluded_neighbors[current_col].add(current_row)
                    continue
                current_col -= 1
                current_row = path_stack[-1]
                continue

            neighbors.sort(reverse=True, key=lambda x: x[0])
            selected_value, selected_row = neighbors[0]

            visited_stack.append((selected_row, current_col + 1))
            result_stack.append(selected_value)
            path_stack.append(selected_row)

            current_row = selected_row
            current_col += 1

        return sum(result_stack), [row + 1 for row in path_stack]

    def find_max_happiness_dp(self, grid):
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
                        dp[i - 1][j - 1] - 1 if dp[i - 1][j - 1] != BLOCKED_CELL else NEG_INFINITY,
                        dp[i][j - 1] + 1 if dp[i][j - 1] != BLOCKED_CELL else NEG_INFINITY,
                        dp[i + 1][j - 1] - 1 if dp[i + 1][j - 1] != BLOCKED_CELL else NEG_INFINITY
                    )
                elif i == 0 and i < m - 1:
                    max_prev = max(
                        dp[i][j - 1] + 1 if dp[i][j - 1] != BLOCKED_CELL else NEG_INFINITY,
                        dp[i + 1][j - 1] - 1 if dp[i + 1][j - 1] != BLOCKED_CELL else NEG_INFINITY
                    )
                elif i == m - 1:
                    max_prev = max(
                        dp[i - 1][j - 1] - 1 if dp[i - 1][j - 1] != BLOCKED_CELL else NEG_INFINITY,
                        dp[i][j - 1] + 1 if dp[i][j - 1] != BLOCKED_CELL else NEG_INFINITY
                    )

                dp[i][j] = cell_value + max_prev if max_prev != NEG_INFINITY else NEG_INFINITY

        max_happiness = max(dp[i][n - 1] for i in range(m))
        path = self.backtrack_path(dp, grid, n, m)

        return max_happiness, path

    @staticmethod
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


if __name__ == "__main__":
    m, n = map(int, input("Enter grid dimensions (m n): ").split())

    grid = []
    print("Enter the grid row by row (each row separated by space):")

    for i in range(m):
        row_input = input(f"Row {i + 1}: ").split()
        row = []
        for cell in row_input:
            if cell == REFRIGERATION_SYMBOL:
                row.append(REFRIGERATION_POINT)
            elif cell == BLOCKED_SYMBOL:
                row.append(BLOCKED_CELL)
            else:
                try:
                    row.append(int(cell))
                except ValueError:
                    print(f"Invalid input '{cell}' in row {i + 1}. Please enter valid grid values.")
                    exit(1)
        grid.append(row)

    phase3 = MaxHappinessPhase3()

    greedy_result, greedy_path = phase3.find_max_happiness_greedy(grid)
    dp_result, dp_path = phase3.find_max_happiness_dp(grid)

    print("\nGreedy Approach:")
    print(f"Max Happiness: {greedy_result}")
    print(f"Path: {greedy_path}")

    print("\nDynamic Programming Approach:")
    print(f"Max Happiness: {dp_result}")
    print(f"Path: {dp_path}")
