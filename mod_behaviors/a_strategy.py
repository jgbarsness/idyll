from abc import ABC, abstractmethod


class CommandStrategy(ABC):
    'interface for strategies to be called on collection'

    @abstractmethod
    def call_command(self, collections: list, title: str, path: str):
        pass
