from abc import ABC, abstractmethod


class MaxHappinessInterface(ABC):

    @abstractmethod
    def find_max_happiness_greedy(self, grid):
        """
        Method to calculate max happiness and path using the Greedy approach.
        Should return a tuple of (max_happiness, path).
        """
        pass

    @abstractmethod
    def find_max_happiness_dp(self, grid):
        """
        Method to calculate max happiness and path using the DP approach.
        Should return a tuple of (max_happiness, path).
        """
        pass

    @property
    @abstractmethod
    def input_path(self):
        """
        Property to return the input file path.
        """
        pass

    @property
    @abstractmethod
    def output_path(self):
        """
        Property to return the output file path.
        """
        pass
