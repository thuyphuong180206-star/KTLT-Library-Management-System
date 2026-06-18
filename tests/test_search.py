"""
Kiểm thử các hàm tìm kiếm sách (Unit Test — Search)
Nhiệm vụ: Xác thực search_by_id, search_by_title, search_by_author, search_by_genre.
Dữ liệu mẫu: tests/data_test/books.csv (7 sách, dùng chung cho mọi file test).
Các test case:
    search_by_id:
        - test_search_by_id_found
        - test_search_by_id_not_found
    search_by_title (áp dụng đều cho author/genre):
        - test_search_by_title_partial_match
        - test_search_by_title_case_insensitive
        - test_search_by_title_no_match
        - test_search_by_title_strips_whitespace
        - test_search_by_title_returns_custom_list
    search_by_author:
        - test_search_by_author_partial_match
        - test_search_by_author_case_insensitive
        - test_search_by_author_no_match
        - test_search_by_author_strips_whitespace
        - test_search_by_author_returns_custom_list
    search_by_genre:
        - test_search_by_genre_partial_match
        - test_search_by_genre_case_insensitive
        - test_search_by_genre_no_match
        - test_search_by_genre_strips_whitespace
        - test_search_by_genre_returns_custom_list
Import: logic.search, structure.custom_list.CustomList, tests.data_loader
"""
import unittest

from structure.custom_list import CustomList
from logic import search
from . import data_loader


class SearchTestCase(unittest.TestCase):
    def setUp(self):
        self.hash_map = data_loader.load_books()

    def _ids(self, result):
        return {book.book_id for book in result}

    # ------------------------------------------------------------------ #
    # search_by_id
    # ------------------------------------------------------------------ #

    def test_search_by_id_found(self):
        book = search.search_by_id(self.hash_map, "B001")
        self.assertIsNotNone(book)
        self.assertEqual(book.title, "Lap Trinh Python Co Ban")

    def test_search_by_id_not_found(self):
        book = search.search_by_id(self.hash_map, "B999")
        self.assertIsNone(book)

    # ------------------------------------------------------------------ #
    # search_by_title
    # ------------------------------------------------------------------ #

    def test_search_by_title_partial_match(self):
        result = search.search_by_title(self.hash_map, "Java")
        self.assertEqual(self._ids(result), {"B002"})

    def test_search_by_title_case_insensitive(self):
        result = search.search_by_title(self.hash_map, "PYTHON")
        self.assertEqual(self._ids(result), {"B001", "B006"})

    def test_search_by_title_no_match(self):
        result = search.search_by_title(self.hash_map, "Khong Ton Tai")
        self.assertEqual(len(result), 0)

    def test_search_by_title_strips_whitespace(self):
        result = search.search_by_title(self.hash_map, "  Java  ")
        self.assertEqual(self._ids(result), {"B002"})

    def test_search_by_title_returns_custom_list(self):
        result = search.search_by_title(self.hash_map, "Java")
        self.assertIsInstance(result, CustomList)

    # ------------------------------------------------------------------ #
    # search_by_author
    # ------------------------------------------------------------------ #

    def test_search_by_author_partial_match(self):
        result = search.search_by_author(self.hash_map, "Rowling")
        self.assertEqual(self._ids(result), {"B004"})

    def test_search_by_author_case_insensitive(self):
        result = search.search_by_author(self.hash_map, "NGUYEN")
        self.assertEqual(self._ids(result), {"B001", "B003", "B005"})

    def test_search_by_author_no_match(self):
        result = search.search_by_author(self.hash_map, "Tolkien")
        self.assertEqual(len(result), 0)

    def test_search_by_author_strips_whitespace(self):
        result = search.search_by_author(self.hash_map, "  Rowling  ")
        self.assertEqual(self._ids(result), {"B004"})

    def test_search_by_author_returns_custom_list(self):
        result = search.search_by_author(self.hash_map, "Rowling")
        self.assertIsInstance(result, CustomList)

    # ------------------------------------------------------------------ #
    # search_by_genre
    # ------------------------------------------------------------------ #

    def test_search_by_genre_partial_match(self):
        result = search.search_by_genre(self.hash_map, "Nghe")
        self.assertEqual(self._ids(result), {"B001", "B002", "B006", "B007"})

    def test_search_by_genre_case_insensitive(self):
        result = search.search_by_genre(self.hash_map, "CONG NGHE")
        self.assertEqual(self._ids(result), {"B001", "B002", "B006", "B007"})

    def test_search_by_genre_no_match(self):
        result = search.search_by_genre(self.hash_map, "Lich Su")
        self.assertEqual(len(result), 0)

    def test_search_by_genre_strips_whitespace(self):
        result = search.search_by_genre(self.hash_map, "  Nghe  ")
        self.assertEqual(self._ids(result), {"B001", "B002", "B006", "B007"})

    def test_search_by_genre_returns_custom_list(self):
        result = search.search_by_genre(self.hash_map, "Nghe")
        self.assertIsInstance(result, CustomList)


if __name__ == "__main__":
    unittest.main()
