# src/phase1/main.py

# Import necessary functions
from src.phase1.utils import read_input, write_output


def find_max_happiness(grid):
    m, n = len(grid), len(grid[0])
    dp = [[0] * n for _ in range(m)]
    for c in range(m):
        dp[c][0] = grid[c][0]
    for j in range(1, n):
        for i in range(m):
            max_prev = 0
            if 0 < i < m - 1:
                max_prev = max(dp[i - 1][j - 1], dp[i][j - 1], dp[i + 1][j - 1])
            elif i == 0 and i < m - 1:
                max_prev = max(dp[i][j - 1], dp[i + 1][j - 1])
            elif i == m - 1:
                max_prev = max(dp[i - 1][j - 1], dp[i][j - 1])

            dp[i][j] = grid[i][j] + max_prev

    max_happiness = max(dp[i][n - 1] for i in range(m))

    # TODO: Find the path that gives the maximum happiness
    path = [0] * n
    # Find the row with the maximum happiness in the last column
    end_row = max(range(m), key=lambda x: dp[x][n - 1])
    path[n - 1] = end_row + 1  # Convert to 1-based index

    # Backtrack to reconstruct the path
    for j in range(n - 1, 0, -1):
        if end_row > 0 and dp[end_row - 1][j - 1] == dp[end_row][j] - grid[end_row][j]:
            end_row -= 1
        elif end_row < m - 1 and dp[end_row + 1][j - 1] == dp[end_row][j] - grid[end_row][j]:
            end_row += 1
        # Otherwise, stay in the same row
        path[j - 1] = end_row + 1  # Convert to 1-based index

    return max_happiness, path


def main():
    input_file = "input/sample_inputs.txt"
    output_file = "output/sample_outputs.txt"

    # Read input grids
    grids = read_input(input_file)

    # Process each grid and calculate results
    results = []
    for _, _, grid in grids:
        max_happiness, path = find_max_happiness(grid)
        results.append((max_happiness, path))

        # Write results to the output file
        write_output(output_file, results)


if __name__ == "__main__":
    main()
