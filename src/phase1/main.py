# src/phase1/main.py

def find_max_happiness(grid):
    m, n = len(grid), len(grid[0])
    dp = [[0] * n for _ in range(m)]
    for i in range(1, m):
        for j in range(n):
            dp[i - 1][j] = grid[i][j] + max(dp[i - 1][j], dp[i - 1][j - 1])
            print(dp[i - 1][j])


sample_input = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
find_max_happiness(sample_input)
