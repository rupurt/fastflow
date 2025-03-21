from dataclasses import dataclass
from typing import Callable


@dataclass
class QueueTrigger:
    func: Callable

    def __str__(self):
        return f"queue:{self.func.__name__}"
