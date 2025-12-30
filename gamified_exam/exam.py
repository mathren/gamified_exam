import difflib
import json
from dataclasses import dataclass
from typing import List, Tuple
from .question import QuestionType, Difficulty, Question
from .grader import TextParser, NumericParser, MultichoiceParser, ListParser, QuantityParser
from enum import Enum
import sys


class GamifiedExam:
    def __init__(self, answers_file: str, tolerance_default=0.05):
        """Initialize exam with answers from a text file."""
        self.questions = []
        self.current_difficulty = Difficulty.BEGINNER
        self.score = 0
        self.max_score = 0
        self.correct_streak = 0
        # Register parsers
        self.parsers: Dict[QuestionType, AnswerParser] = {
            QuestionType.TEXT: TextParser(),
            QuestionType.NUMERIC: NumericParser(tolerance=tolerance_default),
            QuestionType.MULTICHOICE: MultichoiceParser(),
            QuestionType.QUANTITY: QuantityParser(tolerance=tolerance_default),
            QuestionType.LIST: ListParser(),
        }
        self.load_questions(answers_file)

    def register_parser(self, question_type: QuestionType, parser: AnswerParser):
        """Register a custom parser for a question type."""
        self.parsers[question_type] = parser


    def load_questions(self, filename: str):
        """Load questions from text file.

        Format per line: difficulty|points|question_type|prompt|answer, comments with #
        Example: BEGINNER|10|text|Translate: Hello|Hola
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        # skip comments
                        continue

                    parts = line.split('|')
                    if len(parts) != 5:
                        print("line with incorrect question formatting found!")
                        if "debug" in sys.argv:
                            raise ValueError(f"Malformatted question file? (expected 5 parts, got {len(parts)})")
                        else:
                            print(f"Malformatted question file? (expected 5 parts, got {len(parts)})")
                            continue

                    diff, points, question_type, prompt, answer = parts

                    try:
                        self.questions.append(Question(
                            prompt=prompt.strip(),
                            answer=answer.strip(),
                            difficulty=Difficulty[diff.strip().upper()],
                            points=int(points.strip()),
                            question_type=QuestionType[question_type.strip().upper()]
                        ))
                    except (KeyError, ValueError) as e:
                        if "debug" in sys.argv:
                            raise e
                        else:
                            print(f"Line {line_num}: Invalid value - {e}")
                        continue
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")


    def grade_answer(self, user_answer: str, question: Question) -> Tuple[bool, float, str]:
        """Grade an answer using the appropriate parser."""
        parser = self.parsers.get(question.question_type)
        if parser is None:
            return False, 0.0, f"Unknown question type: {question.question_type}"
        return parser.parse(user_answer, question.answer)


    def update_difficulty(self):
        """Update difficulty based on performance."""
        if self.correct_streak >= 3 and self.current_difficulty != Difficulty.ADVANCED:
            if self.current_difficulty == Difficulty.BEGINNER:
                self.current_difficulty = Difficulty.INTERMEDIATE
                print("\n🎉 Level up! Moving to INTERMEDIATE difficulty!")
            elif self.current_difficulty == Difficulty.INTERMEDIATE:
                self.current_difficulty = Difficulty.ADVANCED
                print("\n🎉 Level up! Moving to ADVANCED difficulty!")
            self.correct_streak = 0
        elif self.correct_streak <= -2 and self.current_difficulty != Difficulty.BEGINNER:
            if self.current_difficulty == Difficulty.ADVANCED:
                self.current_difficulty = Difficulty.INTERMEDIATE
                print("\n📉 Moving to INTERMEDIATE difficulty for practice.")
            elif self.current_difficulty == Difficulty.INTERMEDIATE:
                self.current_difficulty = Difficulty.BEGINNER
                print("\n📉 Moving to BEGINNER difficulty for practice.")
            self.correct_streak = 0


    def get_questions_by_difficulty(self, difficulty: Difficulty) -> List[Question]:
        """Get all questions of a specific difficulty."""
        return [q for q in self.questions if q.difficulty == difficulty]


    def run_exam(self):
        """Run the interactive exam."""
        print("=" * 60)
        print("DUOLINGO-STYLE LANGUAGE EXAM")
        print("=" * 60)
        print("\nInstructions:")
        print("- Answer each question as accurately as possible")
        print("- Minor typos will receive partial credit")
        print("- Difficulty increases with correct streaks")
        print("- Type 'quit' to exit early\n")

        question_pool = self.questions.copy()
        question_num = 1

        while question_pool:
            # Filter questions by current difficulty
            available = [q for q in question_pool if q.difficulty == self.current_difficulty]

            # If no questions at current difficulty, adjust
            if not available:
                if self.current_difficulty == Difficulty.ADVANCED:
                    self.current_difficulty = Difficulty.INTERMEDIATE
                elif self.current_difficulty == Difficulty.INTERMEDIATE:
                    self.current_difficulty = Difficulty.BEGINNER
                else:
                    print("Run out of questions!")
                    break
                continue

            # Select next question and remove it from current pool
            question = available[0]
            question_pool.remove(question)  # advances while loop

            # Display question
            print(f"\n[Question {question_num}] [{question.difficulty.name}] ({question.points} points)")
            print(f"{question.prompt}")

            user_answer = input("Your answer: ").strip()

            if user_answer.lower() == 'quit':
                print("\nExiting exam early...")
                break

            is_correct, multiplier, feedback = self.grade_answer(user_answer, question)

            earned_points = int(question.points * multiplier)
            self.max_score += question.points

            if is_correct:
                self.score += earned_points
                self.correct_streak += 1
                print(f"✓ {feedback}")
                print(f"  +{earned_points} points")
            else:
                self.correct_streak -= 1
                print(f"✗ {feedback}")
                print(f"  +0 points")

            print("updating difficulty...")
            self.update_difficulty()
            question_num += 1

        self.show_results()


            # # check question type
            # if question.question_type == QuestionType.TEXT:
            #     # call qualitative answer parser
            #     TextParser()
            # elif question.question_type == QuestionType.NUMERIC:
            #     # call quantitative answer parser
            #     print("NUMERIC question")
            # elif question.question_type == QuestionType.MULTICHOICE:
            #     # call textual question answer parser
            #     print("MULTICHOICE question")
            # elif question.question_type == QuestionType.QUANTITY:
            #     # call visual question answer parser
            #     print("QUANTITY question")
            # elif question.question_type == QuestionType.LIST:
            #     # call visual question answer parser
            #     print("LIST question")
            # else:
            #     # Check answer with auto-correct
            #     is_correct, multiplier, feedback = Grader.auto_correct(user_answer, question.answer)
            #     raise ValueError("QuestionType is unrecognized:", question.question_type)


            # earned_points = int(question.points * multiplier)
            # self.max_score += question.points

            # if is_correct:
            #     self.score += earned_points
            #     self.correct_streak += 1
            #     print(f"✓ {feedback}")
            #     print(f"  +{earned_points} points")
            #     print(f" correct streak = {self.correct_streak}")
            # else:
            #     self.correct_streak -= 1
            #     print(f"✗ {feedback}")
            #     print(f"  +0 points")

            # Update difficulty based on streak
            # self.update_difficulty()

            # question_num += 1

        self.show_results()


    def show_results(self):
        """Display final results."""
        print("\n" + "=" * 60)
        print("EXAM COMPLETE!")
        print("=" * 60)

        percentage = (self.score / self.max_score * 100) if self.max_score > 0 else 0

        print(f"\nFinal Score: {self.score}/{self.max_score} ({percentage:.1f}%)")

        if percentage >= 85:
            print("Grade: A - Excellent! 🌟")
        elif percentage >= 70:
            print("Grade: B - Great job! 👏")
        elif percentage >= 50:
            print("Grade: C - Good effort! 👍")
        elif percentage >= 30:
            print("Grade: D - Keep practicing! 📚")
        else:
            print("Grade: E - More study needed. 💪")

        print("\n" + "=" * 60)



if __name__ == "__main__":
    exam = GamifiedExam('exam_questions.txt')
    exam.run_exam()
