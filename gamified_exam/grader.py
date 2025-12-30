import difflib
from typing import Tuple


class Grader:
    """Handles auto-correction and scoring of answers."""

    @staticmethod
    def calculate_similarity(user_answer: str, correct_answer: str) -> float:
        """Calculate similarity ratio between answers."""
        user_norm = user_answer.lower().strip()
        correct_norm = correct_answer.lower().strip()
        return difflib.SequenceMatcher(None, user_norm, correct_norm).ratio()

    @staticmethod
    def auto_correct(user_answer: str, correct_answer: str) -> Tuple[bool, float, str]:
        """Auto-correct with partial credit.
        TODO: trigger for minor errors

        Returns: (is_acceptable, score_multiplier, feedback)
        """
        similarity = Grader.calculate_similarity(user_answer, correct_answer)

        if similarity == 1.0:
            return True, 1.0, "Perfect! ✓"
        elif similarity >= 0.9:
            return True, 0.9, "Almost perfect! Minor typo detected. (90% points)"
        elif similarity >= 0.75:
            return True, 0.7, "Good! Some errors detected. (70% points)"
        elif similarity >= 0.6:
            return True, 0.5, "Acceptable, but many errors. (50% points)"
        else:
            feedback = f"Incorrect. ✗ Correct answer: {correct_answer}"
            return False, 0.0, feedback
