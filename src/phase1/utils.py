def read_input(input_file):
    """
    Reads input from a file and returns a list of grids.
    Each grid is represented as a tuple (m, n, grid).
    Handles input format with example labels like 'Example 1:'.
    """
    grids = []
    with open(input_file, 'r') as file:
        data = file.readlines()

    index = 0
    while index < len(data):
        line = data[index].strip()

        # Skip empty lines or example labels
        if not line or line.startswith("Example"):
            index += 1
            continue

        try:
            # Parse grid dimensions
            dims = line.split()
            if len(dims) != 2:
                raise ValueError("Invalid grid dimensions format.")
            m, n = int(dims[0]), int(dims[1])
            index += 1

            # Parse the grid
            grid = []
            for _ in range(m):
                grid_line = data[index].strip()
                if not grid_line:
                    raise ValueError("Unexpected empty line in grid data.")
                grid.append(list(map(int, grid_line.split())))
                index += 1

            # Add parsed grid to the list
            grids.append((m, n, grid))

        except (ValueError, IndexError) as e:
            print(f"Error parsing input at line {index + 1}: {e}")
            index += 1  # Skip to the next line to continue parsing

    return grids

def write_output(output_file, results):
    """
    Writes results to a file.
    Each result is a tuple (max_happiness, path).
    """
    with open(output_file, 'w') as file:
        for max_happiness, path in results:
            file.write(f"{max_happiness}\n")
            file.write(f"{path}\n\n")
