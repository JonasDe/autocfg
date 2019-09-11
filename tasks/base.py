from abc import ABC, abstractmethod


class Task(ABC):
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def run(self, *args, **kwargs):
        if
        self
