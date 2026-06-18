"""
Kiểm thử xác thực dữ liệu đầu vào (Unit Test — Validator)
Nhiệm vụ: Xác thực validate_user_id, validate_non_empty, validate_quantity, validate_password.
Các test case:
    validate_user_id:
        - test_validate_user_id_student_8_digits
        - test_validate_user_id_student_9_digits
        - test_validate_user_id_lecturer
        - test_validate_user_id_invalid_format
        - test_validate_user_id_too_short
        - test_validate_user_id_strips_whitespace
    validate_non_empty:
        - test_validate_non_empty_all_filled
        - test_validate_non_empty_has_blank
        - test_validate_non_empty_has_whitespace_only
        - test_validate_non_empty_empty_dict
    validate_quantity:
        - test_validate_quantity_valid_positive
        - test_validate_quantity_zero
        - test_validate_quantity_negative
        - test_validate_quantity_non_numeric
        - test_validate_quantity_strips_whitespace
    validate_password:
        - test_validate_password_valid
        - test_validate_password_too_short
        - test_validate_password_exactly_min_length
        - test_validate_password_strips_whitespace_before_check
Import: interface.validator
"""
import unittest

from interface import validator


class ValidatorTestCase(unittest.TestCase):
    # ------------------------------------------------------------------ #
    # validate_user_id
    # ------------------------------------------------------------------ #

    def test_validate_user_id_student_8_digits(self):
        self.assertEqual(validator.validate_user_id("20211234"), "student")

    def test_validate_user_id_student_9_digits(self):
        self.assertEqual(validator.validate_user_id("202112345"), "student")

    def test_validate_user_id_lecturer(self):
        self.assertEqual(validator.validate_user_id("002.123.45678"), "lecturer")

    def test_validate_user_id_invalid_format(self):
        self.assertIsNone(validator.validate_user_id("abc123"))

    def test_validate_user_id_too_short(self):
        self.assertIsNone(validator.validate_user_id("1234567"))

    def test_validate_user_id_strips_whitespace(self):
        self.assertEqual(validator.validate_user_id("  20211234  "), "student")

    # ------------------------------------------------------------------ #
    # validate_non_empty
    # ------------------------------------------------------------------ #

    def test_validate_non_empty_all_filled(self):
        self.assertTrue(validator.validate_non_empty({"name": "A", "age": "20"}))

    def test_validate_non_empty_has_blank(self):
        self.assertFalse(validator.validate_non_empty({"name": "", "age": "20"}))

    def test_validate_non_empty_has_whitespace_only(self):
        self.assertFalse(validator.validate_non_empty({"name": "   "}))

    def test_validate_non_empty_empty_dict(self):
        self.assertTrue(validator.validate_non_empty({}))

    # ------------------------------------------------------------------ #
    # validate_quantity
    # ------------------------------------------------------------------ #

    def test_validate_quantity_valid_positive(self):
        self.assertTrue(validator.validate_quantity("5"))

    def test_validate_quantity_zero(self):
        self.assertFalse(validator.validate_quantity("0"))

    def test_validate_quantity_negative(self):
        self.assertFalse(validator.validate_quantity("-5"))

    def test_validate_quantity_non_numeric(self):
        self.assertFalse(validator.validate_quantity("abc"))

    def test_validate_quantity_strips_whitespace(self):
        self.assertTrue(validator.validate_quantity("  5  "))

    # ------------------------------------------------------------------ #
    # validate_password
    # ------------------------------------------------------------------ #

    def test_validate_password_valid(self):
        self.assertTrue(validator.validate_password("abcdef"))

    def test_validate_password_too_short(self):
        self.assertFalse(validator.validate_password("abc"))

    def test_validate_password_exactly_min_length(self):
        self.assertTrue(validator.validate_password("123456"))

    def test_validate_password_strips_whitespace_before_check(self):
        self.assertFalse(validator.validate_password("  abc  "))


if __name__ == "__main__":
    unittest.main()
