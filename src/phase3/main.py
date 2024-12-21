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
        return 0, []

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
        pass
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
