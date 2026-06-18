"""
Kiểm thử giải thuật Quick Sort (Unit Test — Sort)
Nhiệm vụ: Xác thực giải thuật quicksort sắp xếp đúng thứ tự A-Z.
Các test case:
    - test_sort_empty_list             : Danh sách rỗng → trả về rỗng
    - test_sort_single_book            : Một sách → trả về nguyên
    - test_sort_alphabetical_by_title  : Nhiều sách, key mặc định "title" → đúng thứ tự A-Z
    - test_sort_same_title             : Sách trùng tên → không lỗi, không mất sách
    - test_sort_by_author              : key="author" → sắp theo tác giả
    - test_sort_by_publisher           : key="publisher" → sắp theo nhà xuất bản
    - test_sort_case_insensitive       : Tên hoa/thường lẫn lộn vẫn sắp đúng
    - test_sort_does_not_mutate_original: Danh sách gốc không bị thay đổi sau khi gọi quicksort
    - test_sort_unknown_key_falls_back_to_title: key lạ → tự dùng "title" làm mặc định
Import: logic.sort, objects.books.Book
"""
import unittest

from objects.books import Book
from logic import sort


def _make_book(book_id, title, author="Tac Gia", publisher="NXB"):
    return Book(book_id, title, author, "The Loai", publisher)


class SortTestCase(unittest.TestCase):
    def test_sort_empty_list(self):
        result = sort.quicksort([], key="title")
        self.assertEqual(result, [])

    def test_sort_single_book(self):
        book = _make_book("B001", "Mot Minh")
        result = sort.quicksort([book], key="title")
        self.assertEqual(result, [book])

    def test_sort_alphabetical_by_title(self):
        b1 = _make_book("B001", "Zen Va Nghe Thuat")
        b2 = _make_book("B002", "Anh Hung")
        b3 = _make_book("B003", "Muoi")
        result = sort.quicksort([b1, b2, b3], key="title")
        self.assertEqual([b.title for b in result], ["Anh Hung", "Muoi", "Zen Va Nghe Thuat"])

    def test_sort_same_title(self):
        b1 = _make_book("B001", "Trung Ten")
        b2 = _make_book("B002", "Trung Ten")
        result = sort.quicksort([b1, b2], key="title")
        self.assertEqual(len(result), 2)
        self.assertEqual({b.book_id for b in result}, {"B001", "B002"})

    def test_sort_by_author(self):
        b1 = _make_book("B001", "Sach A", author="Nguyen Van Z")
        b2 = _make_book("B002", "Sach B", author="Le Thi A")
        result = sort.quicksort([b1, b2], key="author")
        self.assertEqual([b.book_id for b in result], ["B002", "B001"])

    def test_sort_by_publisher(self):
        b1 = _make_book("B001", "Sach A", publisher="NXB Z")
        b2 = _make_book("B002", "Sach B", publisher="NXB A")
        result = sort.quicksort([b1, b2], key="publisher")
        self.assertEqual([b.book_id for b in result], ["B002", "B001"])

    def test_sort_case_insensitive(self):
        b1 = _make_book("B001", "anh hung")
        b2 = _make_book("B002", "Bao Gio")
        result = sort.quicksort([b1, b2], key="title")
        self.assertEqual([b.book_id for b in result], ["B001", "B002"])

    def test_sort_does_not_mutate_original(self):
        b1 = _make_book("B001", "Zen")
        b2 = _make_book("B002", "Anh")
        original = [b1, b2]
        sort.quicksort(original, key="title")
        self.assertEqual(original, [b1, b2])

    def test_sort_unknown_key_falls_back_to_title(self):
        b1 = _make_book("B001", "Zen")
        b2 = _make_book("B002", "Anh")
        result = sort.quicksort([b1, b2], key="khong_ton_tai")
        self.assertEqual([b.title for b in result], ["Anh", "Zen"])


if __name__ == "__main__":
    unittest.main()
