from dataclasses import dataclass
from typing import Callable


@dataclass
class HttpGetTrigger:
    func: Callable

    def __str__(self):
        return f"http-get:{self.func.__name__}"
