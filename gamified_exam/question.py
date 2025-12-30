from dataclasses import dataclass
from enum import Enum


class QuestionType(Enum):
    """ different type of questions"""
    TEXT = 0
    NUMERIC= 1
    MULTICHOICE = 2
    QUANTITY = 3
    LIST = 4
    GRAPH = 5


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
