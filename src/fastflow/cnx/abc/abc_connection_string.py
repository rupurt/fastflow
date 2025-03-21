from dataclasses import dataclass


@dataclass
class ABCConnectionString:
    def __str__(self):
        raise NotImplementedError

    def mode(self, _read_only: bool):
        raise NotImplementedError
