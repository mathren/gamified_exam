"""
Exam Package
A Duolingo-style adaptive examination system
"""

from .exam import GamifiedExam
from .question import Question, Difficulty, QuestionType
from .grader import TextParser, MultichoiceParser, ListParser, QuantityParser

__version__ = "0.1.0"
__all__ = ["GamifiedExam", "Difficulty", "Question", "QuestionType",
           "TextParser", "MultichoiceParser", "ListParser",
           "QuantityParser"]
