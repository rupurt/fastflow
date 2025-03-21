from dataclasses import dataclass
from typing import Callable


@dataclass
class HttpPostTrigger:
    func: Callable

    def __str__(self):
        return f"http-post:{self.func.__name__}"
