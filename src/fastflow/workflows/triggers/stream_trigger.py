from dataclasses import dataclass
from typing import Callable


@dataclass
class StreamTrigger:
    func: Callable

    def __str__(self):
        return f"stream:{self.func.__name__}"
