def find_max_happiness(grid):
    m, n = len(grid), len(grid[0])
    dp = [[0] * n for _ in range(m)]  # Initialize DP table with zero values

    # Initialize the first column
    for c in range(m):
        # Convert "X" to -1 for invalid cells
        if grid[c][0] == "X":
            dp[c][0] = -1
        else:
            dp[c][0] = 0 if grid[c][0] == "O" else grid[c][0]  # Convert "O" to 0

    # Fill the DP table
    for j in range(1, n):
        for i in range(m):
            # Convert "X" and "O" in the grid
            if grid[i][j] == "X":
                dp[i][j] = -1  # Mark as invalid
                continue
            cell_value = 0 if grid[i][j] == "O" else grid[i][j]  # "O" becomes 0
            
            max_prev = float('-inf')  # To ensure valid paths are considered
            if 0 < i < m - 1:
                max_prev = max(
                    dp[i - 1][j - 1] if dp[i - 1][j - 1] != -1 else float('-inf'),
                    dp[i][j - 1] if dp[i][j - 1] != -1 else float('-inf'),
                    dp[i + 1][j - 1] if dp[i + 1][j - 1] != -1 else float('-inf')
                )
            elif i == 0 and i < m - 1:
                max_prev = max(
                    dp[i][j - 1] if dp[i][j - 1] != -1 else float('-inf'),
                    dp[i + 1][j - 1] if dp[i + 1][j - 1] != -1 else float('-inf')
                )
            elif i == m - 1:
                max_prev = max(
                    dp[i - 1][j - 1] if dp[i - 1][j - 1] != -1 else float('-inf'),
                    dp[i][j - 1] if dp[i][j - 1] != -1 else float('-inf')
                )

            # Update DP table only if there's a valid previous path
            dp[i][j] = cell_value + max_prev if max_prev != float('-inf') else -1

    # Find the maximum happiness in the last column
    return max(dp[i][n - 1] for i in range(m) if dp[i][n - 1] != -1)

grid = [
    [42, 13, "X", 74],
    ["X", "X", 25, "X"],
    [6, 99, 58, "O"],
    ["X", "X", "X", 10]
]
print(find_max_happiness(grid))  # Should output 204
