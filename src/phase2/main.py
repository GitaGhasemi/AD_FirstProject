import os

from src.interfaces.max_happiness_interface import MaxHappinessInterface
from src.constants import *

class MaxHappinessPhase2(MaxHappinessInterface):
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

    # Greedy approach to find the maximum happiness and the path
    def find_max_happiness_greedy(self, grid):
        m, n = len(grid), len(grid[0])
        visited_stack = []  # Stack to track visited cells
        result_stack = [] # Stack to store the happiness values
        path_stack = [] # Stack to store the path (row indices)
        excluded_neighbors = [set() for _ in range(n)] # To track excluded neighbors in each column

        # Rollback function to backtrack when no valid move is possible
        def rollback():
            if result_stack:
                result_stack.pop()  # Remove the last happiness value
            if path_stack:
                row = path_stack.pop()  # Remove the last row from path
                col = len(path_stack)  # Get current column index
                excluded_neighbors[col].add(row)  # Exclude the row for the current column
            if visited_stack:
                visited_stack.pop()  # Remove last visited cell

        # Check if the cell is valid (within bounds and not blocked)
        def is_valid_cell(row, col):
            return 0 <= row < m and grid[row][col] != BLOCKED_CELL

        # Function to get the next valid starting row
        def get_next_start():
            selected_row_index = None
            max_value = NEG_INFINITY
            latest_zero_index = None

            for row in range(m):
                # If row is not excluded and the cell is not blocked
                if row not in excluded_neighbors[0] and grid[row][0] != BLOCKED_CELL:
                    value = grid[row][0]
                    if value > max_value:
                        max_value = value
                        selected_row_index = row
                if grid[row][0] == 0:
                    latest_zero_index = row

            if selected_row_index is None:
                selected_row_index = latest_zero_index

            return selected_row_index

        current_col = 0
        current_row = get_next_start()

        if current_row is None:
            return 0, []

        visited_stack.append((current_row, current_col))
        result_stack.append(grid[current_row][current_col])
        path_stack.append(current_row)

        # Greedy approach to move through the grid
        while current_col < n - 1:
            neighbors = []
            # Check the neighbors of the current cell (up, down, and straight)
            for delta in [-1, 0, 1]:
                neighbor_row = current_row + delta
                if is_valid_cell(neighbor_row, current_col + 1) and \
                        neighbor_row not in excluded_neighbors[current_col + 1]:
                    value = grid[neighbor_row][current_col + 1]
                    if value != BLOCKED_CELL:
                        neighbors.append((value, neighbor_row))

            if not neighbors:  # If no valid neighbors, perform a rollback
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

            # Sort the neighbors by value (in descending order)
            neighbors.sort(reverse=True, key=lambda x: x[0])
            selected_value, selected_row = neighbors[0]

            # Add the selected neighbor to the stacks
            visited_stack.append((selected_row, current_col + 1))
            result_stack.append(selected_value)
            path_stack.append(selected_row)

            current_row = selected_row
            current_col += 1

        return sum(result_stack), [row + 1 for row in path_stack]

    # Dynamic Programming approach to find the maximum happiness and the path
    def find_max_happiness_dp(self, grid):
        m, n = len(grid), len(grid[0])
        dp = [[NEG_INFINITY] * n for _ in range(m)]

        for c in range(m):
            dp[c][0] = REFRIGERATION_POINT if grid[c][0] == REFRIGERATION_POINT else grid[c][0]

        # DP calculation for the rest of the columns
        for j in range(1, n):
            for i in range(m):
                if grid[i][j] == BLOCKED_CELL:
                    dp[i][j] = NEG_INFINITY
                    continue

                cell_value = REFRIGERATION_POINT if grid[i][j] == REFRIGERATION_POINT else grid[i][j]
                max_prev = NEG_INFINITY

                # Check valid neighbors (left, upper-left, lower-left)
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
        path = self.backtrack_path(dp, grid, n, m)

        return max_happiness, path

    # Backtrack through the DP table to find the optimal path
    @staticmethod
    def backtrack_path(dp, grid, n, m):
        end_row = -1
        max_val = NEG_INFINITY
        for i in range(m):
            if dp[i][n - 1] > max_val:
                max_val = dp[i][n - 1]
                end_row = i
        path = [0] * n
        path[n - 1] = end_row + 1 

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
        row_input = input(f"Row {i+1}: ").split()
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
                    print(f"Invalid input '{cell}' in row {i+1}. Please enter valid grid values.")
                    exit(1)
        grid.append(row)

    phase2 = MaxHappinessPhase2()

    greedy_result, greedy_path = phase2.find_max_happiness_greedy(grid)
    dp_result, dp_path = phase2.find_max_happiness_dp(grid)

    print("\nGreedy Approach:")
    print(f"Max Happiness: {greedy_result}")
    print(f"Path: {greedy_path}")

    print("\nDynamic Programming Approach:")
    print(f"Max Happiness: {dp_result}")
    print(f"Path: {dp_path}")
