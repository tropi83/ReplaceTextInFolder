from dataclasses import dataclass

@dataclass(frozen=True)
class WordPair:
    old: str
    new: str
