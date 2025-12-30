import pytest
from stellar_exam import LanguageExam, AutoGrader, Difficulty

def test_grader_perfect_match():
    grader = AutoGrader()
    is_correct, multiplier, feedback = grader.auto_correct("Hydrogen", "Hydrogen")
    assert is_correct == True
    assert multiplier == 1.0

def test_grader_minor_typo():
    grader = AutoGrader()
    is_correct, multiplier, feedback = grader.auto_correct("Hydrogn", "Hydrogen")
    assert is_correct == True
    assert multiplier >= 0.5

def test_grader_wrong_answer():
    grader = AutoGrader()
    is_correct, multiplier, feedback = grader.auto_correct("Nova", "Supernova")
    assert is_correct == False
    assert multiplier == 0.0
