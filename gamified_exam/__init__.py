"""
Exam Package
A Duolingo-style adaptive examination system
"""

from .exam import GamifiedExam
from .question import Question, Difficulty
from .grader import AutoGrader

__version__ = "0.1.0"
__all__ = ["GamifiedExam", "Difficulty", "Question", "AutoGrader"]
