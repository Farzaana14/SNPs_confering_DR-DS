from abc import ABC, abstractmethod


class Cleaner(ABC):
    """
    An abstract cleaner class. All cleaners must extend this class
    """

    @abstractmethod
    def clean(self, **kwargs):
        """
        Cleans the data
        :param kwargs:
        :return: A tuple contains the file name and dataframe
        """
        pass
