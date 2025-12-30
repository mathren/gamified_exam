"""
Exam Package
A Duolingo-style adaptive examination system
"""

from .exam import GamifiedExam
from .question import Question, Difficulty
from .grader import Grader

__version__ = "0.1.0"
__all__ = ["GamifiedExam", "Difficulty", "Question", "QuestionType", "Grader"]
