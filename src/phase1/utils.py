def read_input(input_file):
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
        m, n = int(dims[0]), int(dims[1])
        index += 1

        grid = []
        for _ in range(m):
            grid_line = data[index].strip().split()
            grid.append([
                int(cell) for cell in grid_line
            ])
            index += 1
        grids.append(grid)

    return grids


def write_output(output_file, results, dp_times, dp_memories):
    with open(output_file, 'w') as file:
        for i, result in enumerate(results):
            file.write(f"Example {i + 1}:\n")
            file.write(f"Input:\n[\n")
            for row in result["grid"]:
                file.write(f"    {row},\n")
            file.write(f"]\n\n")

            file.write(f"DP Approach:\n")
            file.write(f"Max Happiness: {result['dp']['max_happiness']}\n")
            file.write(f"Path: {result['dp']['path']}\n\n")

            file.write(f"Greedy Approach:\n")
            file.write(f"Max Happiness: {result['greedy']['max_happiness']}\n")
            file.write(f"Path: {result['greedy']['path']}\n\n")

            dp_time = dp_times[i]  # Assuming dp_times contains the execution times for each example
            dp_memory = dp_memories[i]  # Assuming dp_memories contains the memory usage for each example

            file.write(f"Time Complexity: O(m * n), m={len(result['grid'])}, n={len(result['grid'][0])}, "
                       f"{dp_time * 1000:.3f} milliseconds\n")
            file.write(f"Memory Usage: {dp_memory / 1024:.3f} KB\n\n")