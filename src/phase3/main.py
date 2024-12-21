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
        pass

    def find_max_happiness_dp(self, grid):
        pass

    @staticmethod
    def backtrack_path(dp, grid, n, m):
        pass



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

    phase3 = MaxHappinessPhase3()

    greedy_result, greedy_path = phase3.find_max_happiness_greedy(grid)
    dp_result, dp_path = phase3.find_max_happiness_dp(grid)

    print("\nGreedy Approach:")
    print(f"Max Happiness: {greedy_result}")
    print(f"Path: {greedy_path}")

    print("\nDynamic Programming Approach:")
    print(f"Max Happiness: {dp_result}")
    print(f"Path: {dp_path}")
