from typing import Callable

class ProgressTracker:
    """
    Suivi de progression simple : calcule le pourcentage et appelle un callback.
    """
    def __init__(self, total: int, callback: Callable[[int], None]):
        self.total = total
        self.current = 0
        self.callback = callback

    def advance(self, step: int = 1) -> None:
        self.current += step
        percent = int((self.current / self.total) * 100) if self.total > 0 else 100
        self.callback(percent)
