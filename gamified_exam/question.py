from dataclasses import dataclass
from enum import Enum


class QuestionType(Enum):
    """ different type of questions"""
    QUALITATIVE = 0
    QUANTITATVE = 1
    TEXT = 2
    GRAPH = 3


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
