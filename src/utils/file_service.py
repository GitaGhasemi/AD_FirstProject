from src.constants import *


class FileService:

    @staticmethod
    def read_inputs(input_file):
        grids = []
        with open(input_file, 'r') as file:
            data = file.readlines()

        index = 0
        while index < len(data):
            line = data[index].strip()
            if not line or line.startswith(EXAMPLE_HEADER):
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
                        REFRIGERATION_POINT if cell == REFRIGERATION_SYMBOL
                        else BLOCKED_CELL if cell == BLOCKED_SYMBOL
                        else int(cell)
                        for cell in grid_line
                    ]
                    grid.append(row)
                    index += 1
                grids.append(grid)

        return grids

    @staticmethod
    def write_outputs(output_file, results):
        with open(output_file, 'w') as file:
            for i, result in enumerate(results):
                grid = result["grid"]
                greedy_result = result["greedy"]["max_happiness"]
                greedy_path = result["greedy"]["path"]
                dp_result = result["dp"]["max_happiness"]
                dp_path = result["dp"]["path"]

                # Greedy and DP times and memory need to be fetched separately, as they are not included in the result
                greedy_time = result.get("greedy_time", 0)
                greedy_memory = result.get("greedy_memory", 0)
                dp_time = result.get("dp_time", 0)
                dp_memory = result.get("dp_memory", 0)

                file.write(f"Example {i + 1}:\n")
                file.write("Input:\n[\n")
                for row in grid:
                    file.write(f"    {row},\n")
                file.write("]\n\n")

                file.write("Greedy Approach:\n")
                file.write(f"Max Happiness: {greedy_result}\n")
                file.write(f"Path: {greedy_path}\n")
                file.write(
                    f"Time Complexity: O(m * n), m={len(grid)}, n={len(grid[0])}, {greedy_time * 1000:.3f} milliseconds\n")
                file.write(f"Memory Usage: {greedy_memory / 1024:.3f} KB\n\n")

                file.write("DP Approach:\n")
                file.write(f"Max Happiness: {dp_result}\n")
                file.write(f"Path: {dp_path}\n")
                file.write(
                    f"Time Complexity: O(m * n), m={len(grid)}, n={len(grid[0])}, {dp_time * 1000:.3f} milliseconds\n")
                file.write(f"Memory Usage: {dp_memory / 1024:.3f} KB\n\n")

                file.write("\n")
                file.write("-" * 40)
                file.write("\n")
