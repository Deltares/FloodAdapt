import os
import typing
from abc import ABC, abstractmethod


class IStrategy(ABC):
    @abstractmethod
    def load_file(filepath: typing.Union[str, os.PathLike]):
        """create Strategy from toml file"""
        ...

    @abstractmethod
    def load_dict(data: dict):
        """create Strategy from object, e.g. when initialized from GUI"""
        ...

    @abstractmethod
    def save(self, filepath: typing.Union[str, os.PathLike]):
        """save Strategy.model to a toml file"""
