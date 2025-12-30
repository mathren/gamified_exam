import pytest
import sys
import os
# Add parent directory to path if needed
sys.path.insert(0, os.path.abspath('..'))
import gamified_exam as ge
from gamified_exam.grader import TextParser, MultichoiceParser, ListParser
from gamified_exam.question import QuestionType, Difficulty
import pandas as pd
import matplotlib.pyplot as plt
import astropy.units as u
from astropy.units import Quantity
import numpy as np

def test_initialization(test_pool=True):
    exam = ge.GamifiedExam("../data/exam_questions.txt")
    print("Generated exam", type(exam))
    question_pool = exam.questions.copy()
    if test_pool:
        print("question pool created")
        # Filter questions by difficulty
        available = [q for q in question_pool if q.difficulty == Difficulty.BEGINNER]
        print(f"Found {len(available)} question at {Difficulty.BEGINNER} level")
        available = [q for q in question_pool if q.difficulty == Difficulty.INTERMEDIATE]
        print(f"Found {len(available)} question at {Difficulty.INTERMEDIATE} level")
        available = [q for q in question_pool if q.difficulty == Difficulty.ADVANCED]
        print(f"Found {len(available)} question at {Difficulty.ADVANCED} level")
    return exam, question_pool


# def test_get_all_parsers():
#     exam, question_pool = test_initialization()
#     for question_type in [QuestionType.TEXT, QuestionType.NUMERIC, QuestionType.MULTICHOICE, QuestionType.QUANTITY, QuestionType.LIST, QuestionType.Graph]:
#         questions = [q for q in question_pool if q.question_type == question_type]
#         print(f"Found {len(questions)} text questions of type {question_type}")
#         parser = exam.parsers.get(questions[0].question_type)
#         print(parser)


def test_text_parser_correct():
    exam, question_pool = test_initialization(test_pool=False)
    text_questions = [q for q in question_pool if q.question_type == QuestionType.TEXT]
    print(f"Found {len(text_questions)} text questions")
    question = text_questions[0]
    answer = "OBAFGKM"
    # get examiner
    parser = exam.parsers.get(question.question_type)
    is_correct, score, feedback = parser.parse(answer, question.answer)
    assert is_correct == True
    assert score == 1.0


def test_quantity_parser_correct():
    exam, question_pool = test_initialization(test_pool=False)
    questions = [q for q in question_pool if q.question_type == QuestionType.QUANTITY]
    print(f"Found {len(questions)} text questions for {QuestionType.QUANTITY}")
    question = questions[0] # np.random.choice(questions)
    print(question.prompt)
    print("hint:", question.answer)
    answer = "1.4 Msun"
    # answer = input("answer for testing?")
    parser = exam.parsers.get(question.question_type)
    is_correct, score, feedback = parser.parse(answer, question.answer)
    # print(is_correct)
    # print(score)
    # print(feedback)
    assert is_correct == True
    assert score == 1.0



def test_multichoice_parser_correct():
    exam, question_pool = test_initialization(test_pool=False)
    questions = [q for q in question_pool if q.question_type == QuestionType.MULTICHOICE]
    print(f"Found {len(questions)} text questions for {QuestionType.MULTICHOICE}")
    question = questions[0] # np.random.choice(questions)
    print(question.prompt)
    print("hint:", question.answer)
    answer = "D"
    # answer = input("answer for testing?")
    parser = exam.parsers.get(question.question_type)
    is_correct, score, feedback = parser.parse(answer, question.answer)
    # print(is_correct)
    # print(score)
    # print(feedback)
    assert is_correct == True
    assert score == 1.0


def test_list_parser_correct():
    exam, question_pool = test_initialization(test_pool=False)
    questions = [q for q in question_pool if q.question_type == QuestionType.LIST]
    print(f"Found {len(questions)} text questions for {QuestionType.LIST}")
    question = questions[0] # np.random.choice(questions)
    print(question.prompt)
    print("hint:", question.answer)
    answer = "Black hole, Neutron star, white dwarf"
    # answer = input("answer for testing?")
    parser = exam.parsers.get(question.question_type)
    is_correct, score, feedback = parser.parse(answer, question.answer)
    # print(is_correct)
    # print(score)
    # print(feedback)
    assert is_correct == True
    assert score == 1.0


if __name__ == "__main__":
    # test_text_parser_correct()
    test_list_parser_correct()
