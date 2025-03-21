from dataclasses import dataclass
from typing import Callable


@dataclass
class HttpPatchTrigger:
    func: Callable

    def __str__(self):
        return f"http-patch:{self.func.__name__}"
