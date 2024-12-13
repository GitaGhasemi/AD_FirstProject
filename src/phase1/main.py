# src/phase1/main.py

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
    print(dp[m - 1][n - 1])


sample_input = [
    [3, 2, 1, 7, 8, 9],
    [4, 5, 6, 1, 3, 10],
    [7, 8, 9, 2, 5, 3],
    [6, 5, 4, 9, 8, 7],
    [1, 1, 1, 1, 1, 22]
]
find_max_happiness(sample_input)
