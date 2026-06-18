"""
Kiểm thử xác thực dữ liệu đầu vào (Unit Test — Validator)
Nhiệm vụ: Xác thực validate_user_id, validate_non_empty, validate_quantity, validate_password,
          validate_person_name, validate_book_id, validate_text_length.
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
        - test_validate_quantity_zero_is_valid   : "0" hợp lệ (quy tắc mới: >= 0)
        - test_validate_quantity_negative
        - test_validate_quantity_non_numeric
        - test_validate_quantity_strips_whitespace
    validate_password:
        - test_validate_password_valid
        - test_validate_password_too_short
        - test_validate_password_exactly_min_length
        - test_validate_password_strips_whitespace_before_check
    validate_person_name:
        - test_validate_person_name_valid_with_diacritics
        - test_validate_person_name_rejects_digits
        - test_validate_person_name_too_short
        - test_validate_person_name_too_long
    validate_book_id:
        - test_validate_book_id_valid
        - test_validate_book_id_valid_lowercase
        - test_validate_book_id_wrong_prefix
        - test_validate_book_id_wrong_digit_count
    validate_text_length:
        - test_validate_text_length_within_limit
        - test_validate_text_length_exceeds_default_limit
        - test_validate_text_length_custom_max_len
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

    def test_validate_quantity_zero_is_valid(self):
        self.assertTrue(validator.validate_quantity("0"))

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

    # ------------------------------------------------------------------ #
    # validate_person_name
    # ------------------------------------------------------------------ #

    def test_validate_person_name_valid_with_diacritics(self):
        self.assertTrue(validator.validate_person_name("Nguyễn Văn A"))

    def test_validate_person_name_rejects_digits(self):
        self.assertFalse(validator.validate_person_name("Nguyen Van A1"))

    def test_validate_person_name_too_short(self):
        self.assertFalse(validator.validate_person_name("A"))

    def test_validate_person_name_too_long(self):
        self.assertFalse(validator.validate_person_name("A" * 51))

    # ------------------------------------------------------------------ #
    # validate_book_id
    # ------------------------------------------------------------------ #

    def test_validate_book_id_valid(self):
        self.assertTrue(validator.validate_book_id("B001"))

    def test_validate_book_id_valid_lowercase(self):
        self.assertTrue(validator.validate_book_id("b1024"))

    def test_validate_book_id_wrong_prefix(self):
        self.assertFalse(validator.validate_book_id("X001"))

    def test_validate_book_id_wrong_digit_count(self):
        self.assertFalse(validator.validate_book_id("B12345"))

    # ------------------------------------------------------------------ #
    # validate_text_length
    # ------------------------------------------------------------------ #

    def test_validate_text_length_within_limit(self):
        self.assertTrue(validator.validate_text_length("Sach hay", "Ten sach"))

    def test_validate_text_length_exceeds_default_limit(self):
        self.assertFalse(validator.validate_text_length("A" * 51, "Ten sach"))

    def test_validate_text_length_custom_max_len(self):
        self.assertFalse(validator.validate_text_length("A" * 11, "Ten sach", max_len=10))


if __name__ == "__main__":
    unittest.main()
