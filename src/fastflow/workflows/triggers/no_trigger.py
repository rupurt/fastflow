from dataclasses import dataclass


@dataclass
class NoTrigger:
    def __str__(self):
        return "none"
