from dataclasses import dataclass
from enum import Enum


class Difficulty(Enum):
    BEGINNER = 1
    INTERMEDIATE = 2
    ADVANCED = 3


@dataclass
class Question:
    prompt: str
    answer: str
    difficulty: Difficulty
    points: int
