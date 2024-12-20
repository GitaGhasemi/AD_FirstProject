from src.phase2.constants import REFRIGERATION_POINT, BLOCKED_CELL


def read_inputs(input_file):
    grids = []
    with open(input_file, 'r') as file:
        data = file.readlines()

    index = 0
    while index < len(data):
        line = data[index].strip()
        if not line or line.startswith("Example"):
            index += 1
            continue

        dims = line.split()
        if len(dims) == 2:
            m, n = map(int, dims)
            index += 1
            grid = []
            for _ in range(m):
                grid_line = data[index].strip().split()
                row = [
                    REFRIGERATION_POINT if cell == "O"
                    else BLOCKED_CELL if cell == "X"
                    else int(cell)
                    for cell in grid_line
                ]
                grid.append(row)
                index += 1
            grids.append(grid)

    return grids


def write_outputs(output_file, results):
    with open(output_file, 'w') as file:
        for i, (grid, greedy_result, greedy_path, greedy_time, greedy_memory, dp_result, dp_path, dp_time,
                dp_memory) in enumerate(results):
            file.write(f"Example {i + 1}:\n")
            file.write("Input:\n[\n")
            for row in grid:
                file.write(f"    {row},\n")
            file.write("]\n\n")

            file.write("Greedy Approach:\n")
            file.write(f"Result: {greedy_result}\n")
            file.write(f"Path: {greedy_path}\n")
            file.write(f"Time Complexity: O(m * n), m={len(grid)}, n={len(grid[0])}, {greedy_time * 1000:.3f} milliseconds\n")
            file.write(f"Memory Usage: {greedy_memory / 1024:.3f} KB\n\n")

            file.write("DP Approach:\n")
            file.write(f"Result: {dp_result}\n")
            file.write(f"Path: {dp_path}\n")
            file.write(f"Time Complexity: O(m * n), m={len(grid)}, n={len(grid[0])}, {dp_time * 1000:.3f} milliseconds\n")
            file.write(f"Memory Usage: {dp_memory / 1024:.3f} KB\n\n")