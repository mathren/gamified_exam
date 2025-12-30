import difflib
from dataclasses import dataclass
from typing import Tuple, List, Callable, Dict
from abc import ABC, abstractmethod
import astropy.units as u
from astropy.units import Quantity


class AnswerParser(ABC):
    """Base class for answer parsers."""

    @abstractmethod
    def parse(self, user_answer: str, correct_answer: str) -> Tuple[bool, float, str]:
        """Parse and grade an answer.

        Returns: (is_correct, score_multiplier, feedback)
        """
        pass


class TextParser(AnswerParser):
    """Parser for text-based answers with fuzzy matching: case insensitive and space insensitive"""

    def parse(self, user_answer: str, correct_answer: str) -> Tuple[bool, float, str]:
        user_norm = user_answer.lower().strip()
        correct_norm = correct_answer.lower().strip()
        similarity = difflib.SequenceMatcher(None, user_norm, correct_norm).ratio()

        if similarity == 1.0:
            return True, 1.0, "Perfect! ✓"
        elif similarity >= 0.85:
            return True, 0.85, f"Almost perfect! Minor typo detected (85% points). Correct answer: {correct_answer}"
        elif similarity >= 0.7:
            return True, 0.7, f"Good! Some errors detected (70% points). Correct answer: {correct_answer}"
        elif similarity >= 0.3:
            return True, 0.3, f"Acceptable, but many errors (30% points). Correct answer: {correct_answer}"
        else:
            return False, 0.0, f"Incorrect. ✗ Correct answer: {correct_answer}"


# class NumericParser(AnswerParser):
#     """Parser for numeric answers with tolerance."""

#     def __init__(self, tolerance=0.05):
#         self.tolerance = tolerance

#     def parse(self, user_answer: str, correct_answer: str) -> Tuple[bool, float, str]:
#         try:
#             # Extract numbers from strings
#             user_num = float(re.findall(r'-?\d+\.?\d*', user_answer)[0])
#             correct_num = float(re.findall(r'-?\d+\.?\d*', correct_answer)[0])

#             # Calculate percentage difference
#             if correct_num == 0:
#                 diff_percent = 100 if user_num != 0 else 0
#             else:
#                 diff_percent = abs((user_num - correct_num) / correct_num * 100)

#             if diff_percent == 0:
#                 return True, 1.0, "Perfect! ✓"
#             elif diff_percent <= self.tolerance:
#                 score = 1.0 - (diff_percent / self.tolerance) * 0.2  # Max 20% penalty
#                 return True, score, f"Close! Within {diff_percent:.1f}% ({score*100:.0f}% points)"
#             elif diff_percent <= self.tolerance * 2:
#                 return True, 0.6, f"Acceptable range. ({diff_percent:.1f}% off, 60% points)"
#             else:
#                 return False, 0.0, f"Incorrect. ✗ Correct answer: {correct_answer} (you were {diff_percent:.1f}% off)"
#         except (IndexError, ValueError):
#             return False, 0.0, f"Invalid numeric format. ✗ Correct answer: {correct_answer}"


class MultichoiceParser(AnswerParser):
    """Parser for multiple choice answers (A, B, C, D)."""

    def parse(self, user_answer: str, correct_answer: str) -> Tuple[bool, float, str]:
        user_norm = user_answer.strip().upper()
        correct_norm = correct_answer.strip().upper()

        # Extract just the letter if full text provided
        if len(user_norm) > 1:
            match = re.search(r'[A-D]', user_norm)
            if match:
                user_norm = match.group()

        if user_norm == correct_norm:
            return True, 1.0, "Correct! ✓"
        else:
            return False, 0.0, f"Incorrect. ✗ Correct answer: {correct_answer}"



class ListParser(AnswerParser):
    """Parser for list answers (comma-separated, order doesn't matter)."""

    def parse(self, user_answer: str, correct_answer: str) -> Tuple[bool, float, str]:
        # Split by comma and normalize
        user_items = set(item.strip().lower() for item in user_answer.split(','))
        correct_items = set(item.strip().lower() for item in correct_answer.split(','))

        if user_items == correct_items:
            return True, 1.0, "Perfect! All items correct. ✓"

        # Calculate partial credit
        correct_count = len(user_items & correct_items)
        total_count = len(correct_items)

        if correct_count == 0:
            return False, 0.0, f"Incorrect. ✗ Correct answer: {correct_answer}"

        score = correct_count / total_count
        missing = correct_items - user_items
        extra = user_items - correct_items

        feedback = f"Partial credit: {correct_count}/{total_count} correct ({score*100:.0f}% points)"
        if missing:
            feedback += f"\nMissing: {', '.join(missing)}"
        if extra:
            feedback += f"\nExtra/incorrect: {', '.join(extra)}"

        return True, score, feedback


class QuantityParser(AnswerParser):
    """Parser for quantities with units using astropy.units for proper unit handling."""

    def __init__(self, tolerance=0.05):
        self.tolerance = tolerance


    def parse(self, user_answer: str, correct_answer: str) -> Tuple[bool, float, str]:
        try:
            return self._parse_with_astropy(user_answer, correct_answer)
        except:
            return self._parse_fallback(user_answer, correct_answer)

    def _parse_with_astropy(self, user_answer: str, correct_answer: str) -> Tuple[bool, float, str]:
        """Parse using astropy units for proper unit conversion and validation."""
        try:
            # Parse the correct answer first to establish expected units
            correct_qty = self._parse_quantity(correct_answer)
            if correct_qty is None:
                return False, 0.0, f"Invalid correct answer format: {correct_answer}"

            # Parse user answer
            user_qty = self._parse_quantity(user_answer)
            if user_qty is None:
                return False, 0.0, f"Invalid format. Expected format like: {correct_answer}"

            # Check if units are compatible (can be converted)
            try:
                user_in_correct_units = user_qty.to(correct_qty.unit)
            except u.UnitConversionError:
                return False, 0.0, f"Incompatible units. ✗ Expected units like: {correct_qty.unit}"

            # Calculate percentage difference
            correct_value = correct_qty.value
            user_value = user_in_correct_units.value

            if correct_value == 0:
                diff_percent = 100 if user_value != 0 else 0
            else:
                diff_percent = abs((user_value - correct_value) / correct_value * 100)

            # Grade based on accuracy
            if diff_percent == 0:
                return True, 1.0, "Perfect! ✓"
            elif diff_percent <= self.tolerance:
                score = 1.0 - (diff_percent / self.tolerance) * 0.2
                return True, score, f"Excellent! Within {diff_percent:.1f}% ({score*100:.0f}% points)"
            elif diff_percent <= self.tolerance * 2:
                return True, 0.6, f"Acceptable range. ({diff_percent:.1f}% off, 60% points)"
            else:
                return False, 0.0, f"Incorrect. ✗ Correct answer: {correct_answer} (you were {diff_percent:.1f}% off)"

        except Exception as e:
            return False, 0.0, f"Error parsing answer: {str(e)}"

    def _parse_quantity(self, qty_string: str):
        """Parse a quantity string into an astropy Quantity.

        Handles formats like:
        - "1.4 solar masses" or "1.4 Msun"
        - "5778 K" or "5778 Kelvin"
        - "3.8e26 watts" or "3.8e26 W"
        - "10 km/s" or "10 kilometers per second"
        """
        try:
            qty_string = qty_string.strip()

            # Common astronomy unit replacements
            replacements = {
                'solar masses': 'Msun',
                'solar mass': 'Msun',
                'solar luminosities': 'Lsun',
                'solar luminosity': 'Lsun',
                'solar radii': 'Rsun',
                'solar radius': 'Rsun',
                'earth masses': 'Mearth',
                'earth mass': 'Mearth',
                'jupiter masses': 'Mjup',
                'jupiter mass': 'Mjup',
                'parsecs': 'pc',
                'parsec': 'pc',
                'light years': 'lyr',
                'light year': 'lyr',
                'years': 'yr',
                'year': 'yr',
                'kelvin': 'K',
                'watts': 'W',
                'watt': 'W',
                'meters': 'm',
                'meter': 'm',
                'kilometers': 'km',
                'kilometer': 'km',
                'seconds': 's',
                'second': 's',
            }

            # Apply replacements (case insensitive)
            lower_qty = qty_string.lower()
            for old, new in replacements.items():
                if old in lower_qty:
                    qty_string = qty_string.lower().replace(old, new)
                    break

            # Try to parse with astropy
            return u.Quantity(qty_string)

        except Exception:
            return None

    def _parse_fallback(self, user_answer: str, correct_answer: str) -> Tuple[bool, float, str]:
        """Fallback parser when astropy is not available."""
        print("Astropy fail? Trying fallback parser with regex")
        try:
            user_match = re.match(r'(-?\d+\.?\d*(?:[eE][+-]?\d+)?)\s*(.+)', user_answer.strip())
            correct_match = re.match(r'(-?\d+\.?\d*(?:[eE][+-]?\d+)?)\s*(.+)', correct_answer.strip())

            if not user_match or not correct_match:
                return False, 0.0, f"Invalid format. ✗ Correct answer: {correct_answer}"

            user_num = float(user_match.group(1))
            user_unit = user_match.group(2).lower().strip()
            correct_num = float(correct_match.group(1))
            correct_unit = correct_match.group(2).lower().strip()

            # Check units match
            unit_similarity = difflib.SequenceMatcher(None, user_unit, correct_unit).ratio()
            if unit_similarity < 0.8:
                return False, 0.0, f"Wrong units. ✗ Correct answer: {correct_answer}"

            # Check numeric value
            if correct_num == 0:
                diff_percent = 100 if user_num != 0 else 0
            else:
                diff_percent = abs((user_num - correct_num) / correct_num * 100)

            if diff_percent == 0:
                return True, 1.0, "Perfect! ✓"
            elif diff_percent <= self.tolerance:
                score = 1.0 - (diff_percent / self.tolerance) * 0.2
                return True, score, f"Close! Within {diff_percent:.1f}% ({score*100:.0f}% points)"
            elif diff_percent <= self.tolerance * 2:
                return True, 0.6, f"Acceptable. ({diff_percent:.1f}% off, 60% points)"
            else:
                return False, 0.0, f"Incorrect. ✗ Correct answer: {correct_answer}"
        except (AttributeError, ValueError, IndexError):
            return False, 0.0, f"Invalid format. ✗ Correct answer: {correct_answer}"
