from dataclasses import dataclass
from enum import Enum


class QuestionType(Enum):
    """ different type of questions"""
    TEXT = 0
    QUANTITY = 1
    MULTICHOICE = 2
    LIST = 3
    # GRAPH = 4  # To be implemented


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
    question_type: QuestionType
