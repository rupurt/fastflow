from dataclasses import dataclass
from typing import Callable


@dataclass
class HttpDeleteTrigger:
    func: Callable

    def __str__(self):
        return f"http-delete:{self.func.__name__}"
