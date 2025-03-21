from dataclasses import dataclass
from typing import Callable


@dataclass
class CronTrigger:
    func: Callable
    schedule: str

    def __str__(self):
        return f"cron:{self.func.__name__}({self.schedule})"
