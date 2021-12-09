from abc import ABC, abstractmethod


class AlgorithmExecutor(ABC):
    """
    An abstract algorithm executor class. All algorithm executors must extend this class
    """

    @abstractmethod
    def execute(self, **kwargs):
        """
        Executes a specific statistical/ML algorithm
        :param kwargs:
        :return: A tuple contains the file name and dataframe
        """
        pass
