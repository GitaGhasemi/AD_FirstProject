import time
import tracemalloc

from src.interfaces.max_happiness_interface import MaxHappinessInterface
from src.phase1.main import MaxHappinessPhase1
from src.phase2.main import MaxHappinessPhase2
from src.phase3.main import MaxHappinessPhase3
from src.utils.file_service import FileService

#This is only for the last git commit.   sincerely, git.

class Executor:
    def __init__(self):
        self.interfaces = []  # List to hold interfaces
        self.phases = []  # List to store phases to be executed

    def attach_phase(self, interface_implementation: MaxHappinessInterface):
        """
        Attach an interface (implementation of MaxHappinessInterface) to be executed.
        """
        self.interfaces.append(interface_implementation)

    def execute_phases(self):
        """
        Executes all phases for each attached interface and writes results.
        """
        for interface_implementation in self.interfaces:
            self.process_grids(interface_implementation)

    @staticmethod
    def process_grids(interface_implementation):
        input_path = interface_implementation.input_path
        output_path = interface_implementation.output_path

        grids = FileService.read_inputs(input_path)
        results = []

        for grid in grids:
            # Greedy Approach
            tracemalloc.start()
            start_time = time.time()
            greedy_result, greedy_path = interface_implementation.find_max_happiness_greedy(grid)
            greedy_time = time.time() - start_time
            greedy_memory, _ = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            # DP Approach
            tracemalloc.start()
            start_time = time.time()
            dp_result, dp_path = interface_implementation.find_max_happiness_dp(grid)
            dp_time = time.time() - start_time
            dp_memory, _ = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            # Append the results with the timing and memory information
            results.append({
                "grid": grid,
                "greedy": {
                    "max_happiness": greedy_result,
                    "path": greedy_path,
                },
                "dp": {
                    "max_happiness": dp_result,
                    "path": dp_path,
                },
                "greedy_time": greedy_time,
                "greedy_memory": greedy_memory,
                "dp_time": dp_time,
                "dp_memory": dp_memory
            })

        FileService.write_outputs(output_path, results)


def main():
    # Create the executor instance
    executor = Executor()

    # Instantiate the interface implementation (you can add more implementations if needed)
    phase1 = MaxHappinessPhase1()
    phase2 = MaxHappinessPhase2()
    phase3 = MaxHappinessPhase3()

    # Attach the phase (interface implementation) to the executor
    executor.attach_phase(phase1)
    executor.attach_phase(phase2)
    executor.attach_phase(phase3)

    # Execute all the phases attached to the executor
    executor.execute_phases()


if __name__ == "__main__":
    main()
