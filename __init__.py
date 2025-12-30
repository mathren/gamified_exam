"""
Stellar Evolution Exam Package
A Duolingo-style adaptive examination system for stellar evolution courses.
"""

from .exam import GamifiedExam, Difficulty
from .question import Question
from .grader import AutoGrader

__version__ = "0.1.0"
__all__ = ["GamifiedExam", "Difficulty", "Question", "AutoGrader"]
