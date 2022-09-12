from abc import ABC, abstractmethod


class StatChangeListener(ABC):

    @abstractmethod
    def std_deviation_changed(self, pair: str, old_std_deviation: float, new_std_deviation: float):
        ...
