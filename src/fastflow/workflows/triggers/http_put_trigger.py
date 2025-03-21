from dataclasses import dataclass
from typing import Callable


@dataclass
class HttpPutTrigger:
    func: Callable

    def __str__(self):
        return f"http-put:{self.func.__name__}"
