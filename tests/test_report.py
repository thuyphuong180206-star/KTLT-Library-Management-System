"""
Kiểm thử mô-đun báo cáo thống kê (Unit Test — Report)
Nhiệm vụ: Xác thực get_borrowing_loans, get_overdue_loans, get_top5_books.
Dữ liệu mẫu sách: tests/data_test/books.csv (dùng chung cho mọi file test).
Phiếu mượn/người dùng: dựng trực tiếp trong code (phụ thuộc "hôm nay" để tính quá hạn).
Các test case:
    get_borrowing_loans:
        - test_get_borrowing_loans_includes_only_borrowing_status
        - test_get_borrowing_loans_includes_correct_fields
        - test_get_borrowing_loans_empty_when_none_borrowing
        - test_get_borrowing_loans_unknown_book_title_fallback
    get_overdue_loans:
        - test_get_overdue_loans_auto_promotes_borrowing_past_due
        - test_get_overdue_loans_excludes_not_yet_due
        - test_get_overdue_loans_includes_existing_overdue
        - test_get_overdue_loans_fee_calculation
        - test_get_overdue_loans_excludes_returned
    get_top5_books:
        - test_get_top5_books_returns_top5_by_borrow_count
        - test_get_top5_books_excludes_zero_borrow_count
        - test_get_top5_books_fewer_than_5_eligible
        - test_get_top5_books_returns_custom_list
Import: logic.report, objects.books.Book, objects.users.User, objects.loans.Loan,
        structure.hash_map.BookHashMap, structure.doubly_linked_list.TransactionList,
        structure.user_array.UserArray, structure.priority_queue.PriorityQueue,
        structure.custom_list.CustomList, tests.data_loader
"""
import unittest
from datetime import date, timedelta

from objects.books import Book
from objects.users import User
from objects.loans import Loan
from structure.hash_map import BookHashMap
from structure.doubly_linked_list import TransactionList
from structure.user_array import UserArray
from structure.priority_queue import PriorityQueue
from structure.custom_list import CustomList
from logic import report
from . import data_loader


class ReportLoansTestCase(unittest.TestCase):
    def setUp(self):
        self.hash_map = data_loader.load_books()
        self.dll = TransactionList()
        self.user_array = UserArray()
        self.student = User("U001", "Sinh Vien A", "pass123", role="user", reader_type="student")
        self.user_array.append(self.student)

    def _add_loan(self, user_id, book_id, status="borrowing", borrow_date=None, due_date=None):
        borrow_date = borrow_date or date.today()
        due_date = due_date or (borrow_date + timedelta(days=14))
        loan = Loan(f"L{self.dll.size + 1:03d}", user_id, book_id, borrow_date, due_date=due_date, status=status)
        self.dll.add_transaction(loan)
        return loan

    # ------------------------------------------------------------------ #
    # get_borrowing_loans
    # ------------------------------------------------------------------ #

    def test_get_borrowing_loans_includes_only_borrowing_status(self):
        self._add_loan("U001", "B001", status="borrowing")
        self._add_loan("U001", "B002", status="returned")
        self._add_loan("U001", "B003", status="overdue")
        result = report.get_borrowing_loans(self.dll, self.hash_map)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["book_id"], "B001")

    def test_get_borrowing_loans_includes_correct_fields(self):
        loan = self._add_loan("U001", "B001", status="borrowing")
        result = report.get_borrowing_loans(self.dll, self.hash_map)
        d = result[0]
        self.assertEqual(d["loan_id"], loan.loan_id)
        self.assertEqual(d["user_id"], "U001")
        self.assertEqual(d["title"], "Lap Trinh Python Co Ban")
        self.assertEqual(d["borrow_date"], loan.borrow_date)
        self.assertEqual(d["due_date"], loan.due_date)

    def test_get_borrowing_loans_empty_when_none_borrowing(self):
        self._add_loan("U001", "B001", status="returned")
        self._add_loan("U001", "B002", status="overdue")
        result = report.get_borrowing_loans(self.dll, self.hash_map)
        self.assertEqual(len(result), 0)

    def test_get_borrowing_loans_unknown_book_title_fallback(self):
        self._add_loan("U001", "ZZZZ", status="borrowing")
        result = report.get_borrowing_loans(self.dll, self.hash_map)
        self.assertEqual(result[0]["title"], "Khong ro")

    # ------------------------------------------------------------------ #
    # get_overdue_loans
    # ------------------------------------------------------------------ #

    def test_get_overdue_loans_auto_promotes_borrowing_past_due(self):
        loan = self._add_loan("U001", "B001", status="borrowing", due_date=date.today() - timedelta(days=2))
        result = report.get_overdue_loans(self.dll, self.hash_map, self.user_array)
        self.assertEqual(loan.status, "overdue")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["book_id"], "B001")

    def test_get_overdue_loans_excludes_not_yet_due(self):
        loan = self._add_loan("U001", "B001", status="borrowing", due_date=date.today() + timedelta(days=2))
        result = report.get_overdue_loans(self.dll, self.hash_map, self.user_array)
        self.assertEqual(len(result), 0)
        self.assertEqual(loan.status, "borrowing")

    def test_get_overdue_loans_includes_existing_overdue(self):
        self._add_loan("U001", "B001", status="overdue", due_date=date.today() - timedelta(days=1))
        result = report.get_overdue_loans(self.dll, self.hash_map, self.user_array)
        self.assertEqual(len(result), 1)

    def test_get_overdue_loans_fee_calculation(self):
        self._add_loan("U001", "B001", status="borrowing", due_date=date.today() - timedelta(days=4))
        result = report.get_overdue_loans(self.dll, self.hash_map, self.user_array)
        self.assertEqual(result[0]["days_overdue"], 4)
        self.assertEqual(result[0]["temp_fee"], 4 * 2000)

    def test_get_overdue_loans_excludes_returned(self):
        self._add_loan("U001", "B001", status="returned", due_date=date.today() - timedelta(days=4))
        result = report.get_overdue_loans(self.dll, self.hash_map, self.user_array)
        self.assertEqual(len(result), 0)


class ReportTop5TestCase(unittest.TestCase):
    def setUp(self):
        self.hash_map = data_loader.load_books()
        self.pq = PriorityQueue()

    def test_get_top5_books_returns_top5_by_borrow_count(self):
        result = report.get_top5_books(self.hash_map, self.pq)
        self.assertEqual([b.book_id for b in result], ["B004", "B001", "B003", "B002", "B005"])

    def test_get_top5_books_excludes_zero_borrow_count(self):
        result = report.get_top5_books(self.hash_map, self.pq)
        self.assertNotIn("B006", [b.book_id for b in result])

    def test_get_top5_books_fewer_than_5_eligible(self):
        small_hash_map = BookHashMap()
        small_hash_map.insert("X001", Book("X001", "Sach 1", "Tac Gia", "The Loai", "NXB", borrow_count=5))
        small_hash_map.insert("X002", Book("X002", "Sach 2", "Tac Gia", "The Loai", "NXB", borrow_count=2))
        result = report.get_top5_books(small_hash_map, self.pq)
        self.assertEqual(len(result), 2)

    def test_get_top5_books_returns_custom_list(self):
        result = report.get_top5_books(self.hash_map, self.pq)
        self.assertIsInstance(result, CustomList)


if __name__ == "__main__":
    unittest.main()
