import os

from src.interfaces.max_happiness_interface import MaxHappinessInterface
from src.constants import *


class MaxHappinessPhase1(MaxHappinessInterface):
    def __init__(self, input_path=None, output_path=None):
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

    # Greedy approach for finding maximum happiness path
    def find_max_happiness_greedy(self, grid):
        m, n = len(grid), len(grid[0])
        path_stack = [] # Stores the path (row indices)
        result_stack = [] # Stores the values at each step along the path

        # Find the row with the maximum value in the first column
        max_value = NEG_INFINITY
        current_row = 0
        for i in range(m):
            if grid[i][0] > max_value:
                max_value = grid[i][0]
                current_row = i

        result_stack.append(grid[current_row][0])
        path_stack.append(current_row)

        # Traverse column by column, finding the best next step in each column
        for col in range(1, n):
            neighbors = []
            for delta in [-1, 0, 1]:
                neighbor_row = current_row + delta
                if 0 <= neighbor_row < m:
                    neighbors.append((grid[neighbor_row][col], neighbor_row))

            # Find the maximum neighbor value and move to that row
            max_value = NEG_INFINITY
            selected_row = current_row
            for value, row in neighbors:
                if value > max_value:
                    max_value = value
                    selected_row = row

            result_stack.append(max_value)
            path_stack.append(selected_row)
            current_row = selected_row

        return sum(result_stack), [row + 1 for row in path_stack]

    # Dynamic Programming approach for finding maximum happiness path
    def find_max_happiness_dp(self, grid):
        m, n = len(grid), len(grid[0])
        dp = [[0] * n for _ in range(m)] # DP table to store maximum happiness values

        # Initialize the first column of the DP table
        for c in range(m):
            dp[c][0] = grid[c][0]

        # Fill the DP table by storing the sum of the maximum value from neighboring cells and current value
        for j in range(1, n): # Iterate over columns starting from the second column
            for i in range(m): # Iterate over rows
                max_prev = 0

                 # Check the valid neighbors in the previous column
                if 0 < i < m - 1:
                    max_prev = max(dp[i - 1][j - 1], dp[i][j - 1], dp[i + 1][j - 1])
                elif i == 0 and i < m - 1:
                    max_prev = max(dp[i][j - 1], dp[i + 1][j - 1])
                elif i == m - 1:
                    max_prev = max(dp[i - 1][j - 1], dp[i][j - 1])

                # Store the sum of the current value and the max value of the previous neighbors
                dp[i][j] = grid[i][j] + max_prev

        # Find the maximum happiness and the ending row in the last column
        max_happiness = NEG_INFINITY
        end_row = 0
        for i in range(m):
            if dp[i][n - 1] > max_happiness:
                max_happiness = dp[i][n - 1]
                end_row = i

        # Reconstruct the path by backtracking from the last column
        path = [0] * n
        path[n - 1] = end_row + 1

        for j in range(n - 1, 0, -1):
            # Calculate the possible neighbors from the previous column
            prev_value = dp[end_row][j] - grid[end_row][j]

            # Compare the previous value to neighbors in the previous column and check if it matches
            if end_row > 0 and dp[end_row - 1][j - 1] == prev_value:
                end_row -= 1
            elif end_row < m - 1 and dp[end_row + 1][j - 1] == prev_value:
                end_row += 1
            path[j - 1] = end_row + 1

        return max_happiness, path


if __name__ == "__main__":
    m, n = map(int, input("Enter grid dimensions (m n): ").split())

    grid = []
    print("Enter the grid row by row (each row separated by space):")

    for i in range(m):
        row = list(map(int, input(f"Row {i + 1}: ").split()))
        grid.append(row)

    phase1 = MaxHappinessPhase1()

    greedy_result, greedy_path = phase1.find_max_happiness_greedy(grid)
    dp_result, dp_path = phase1.find_max_happiness_dp(grid)

    print("\nGreedy Approach:")
    print(f"Max Happiness: {greedy_result}")
    print(f"Path: {greedy_path}")

    print("\nDynamic Programming Approach:")
    print(f"Max Happiness: {dp_result}")
    print(f"Path: {dp_path}")
