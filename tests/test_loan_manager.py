"""
Kiểm thử nghiệp vụ mượn/trả sách (Unit Test — Loan Manager)
Nhiệm vụ: Xác thực tính đúng đắn của process_borrow, process_return,
          calculate_overdue_fee, is_book_on_loan, add_to_waiting_queue.
Dữ liệu mẫu: tests/data_test/{books,users,loans,waiting_requests}.csv, nạp đầy đủ
             (không lọc dòng nào) cho mọi test qua tests/data_loader.py — mỗi test
             chỉ thao tác đúng user/sách cần dùng, phần dữ liệu còn lại là "nhiễu"
             giống một hệ thống thật.
Các test case:
    process_borrow:
        - test_borrow_success                  : 20211004 (chưa mượn gì) mượn B005 → thành công
        - test_borrow_user_not_found            : "20219999" không tồn tại → từ chối
        - test_borrow_book_not_found             : "B999" không tồn tại → từ chối
        - test_borrow_overdue_debt              : 002.456.78901 (đang nợ quá hạn L002) → từ chối
        - test_borrow_exceed_limit              : 20211003 (đã mượn đủ 3 cuốn) → từ chối
        - test_borrow_already_borrowing_same_book: 20211001 mượn lại B001 (đang mượn L001) → từ chối
        - test_borrow_inactive_book              : B006 (inactive) → từ chối
        - test_borrow_out_of_stock              : B007 (quantity=0) → từ chối
        - test_borrow_custom_date               : Truyền borrow_date → due_date tính đúng
    process_return:
        - test_return_no_overdue                : 20211001 trả B001 (L001) đúng hạn → phí 0
        - test_return_with_overdue_fee           : Trả trễ 3 ngày (SV) → phí 6.000 VNĐ
        - test_return_custom_date               : Trễ 5 ngày → phí 10.000 VNĐ
        - test_return_loan_not_found            : 20211004 trả B001 (chưa từng mượn) → từ chối
        - test_return_priority_cascade_success  : 20211001 trả B001 → 20211004 (hàng chờ B001) được mượn ngay
        - test_return_priority_cascade_ineligible: 20211003 trả B003 → 002.456.78901 (hàng chờ B003, đang nợ) vẫn ở lại
        - test_return_priority_cascade_no_match : 20211003 trả B002 → không ai chờ B002, sách về kho
    calculate_overdue_fee:
        - test_calculate_overdue_fee_not_due_yet : check_date trước due_date → 0
        - test_calculate_overdue_fee_overdue     : check_date sau due_date 4 ngày → 8.000 VNĐ
        - test_calculate_overdue_fee_returned    : phiếu L006 đã trả → 0
    is_book_on_loan:
        - test_is_book_on_loan_true             : B001 (có L001 borrowing) → True
        - test_is_book_on_loan_false             : B007 (không phiếu nào) → False
    add_to_waiting_queue:
        - test_add_to_waiting_queue_success     : Đăng ký mới (20211003/B005) → thành công
        - test_add_to_waiting_queue_duplicate   : 20211004/B001 đã có sẵn (WR001) → từ chối
        - test_add_to_waiting_queue_custom_date : Truyền request_date → lưu đúng ngày đó
Import: logic.loan_manager, tests.data_loader
"""
import unittest
from datetime import date, timedelta

from logic import loan_manager
from . import data_loader


def _find_loan(dll, user_id, loan_id):
    for loan in dll.get_transactions_by_user(user_id):
        if loan.loan_id == loan_id:
            return loan
    return None


def _find_request(waiting_queue, request_id):
    for request in waiting_queue.to_list():
        if request.request_id == request_id:
            return request
    return None


class LoanManagerTestCase(unittest.TestCase):
    def setUp(self):
        self.hash_map = data_loader.load_books()
        self.dll = data_loader.load_loans()
        self.user_array = data_loader.load_users()
        self.waiting_queue = data_loader.load_waiting_requests()

    # ------------------------------------------------------------------ #
    # process_borrow
    # ------------------------------------------------------------------ #

    def test_borrow_success(self):
        success, msg = loan_manager.process_borrow(
            self.hash_map, self.dll, self.user_array, "20211004", "B005", self.waiting_queue, borrow_date=date(2024, 1, 1)
        )
        self.assertTrue(success)
        book = self.hash_map.search("B005")
        self.assertEqual(book.quantity, 5)
        self.assertEqual(book.borrow_count, 2)
        self.assertEqual(len(self.dll.get_transactions_by_user("20211004")), 1)

    def test_borrow_user_not_found(self):
        success, msg = loan_manager.process_borrow(
            self.hash_map, self.dll, self.user_array, "20219999", "B001", self.waiting_queue, borrow_date=date(2024, 1, 1)
        )
        self.assertFalse(success)

    def test_borrow_book_not_found(self):
        success, msg = loan_manager.process_borrow(
            self.hash_map, self.dll, self.user_array, "20211004", "B999", self.waiting_queue, borrow_date=date(2024, 1, 1)
        )
        self.assertFalse(success)

    def test_borrow_overdue_debt(self):
        success, msg = loan_manager.process_borrow(
            self.hash_map, self.dll, self.user_array, "002.456.78901", "B001", self.waiting_queue, borrow_date=date(2024, 1, 1)
        )
        self.assertFalse(success)

    def test_borrow_exceed_limit(self):
        success, msg = loan_manager.process_borrow(
            self.hash_map, self.dll, self.user_array, "20211003", "B001", self.waiting_queue, borrow_date=date(2024, 1, 1)
        )
        self.assertFalse(success)

    def test_borrow_already_borrowing_same_book(self):
        success, msg = loan_manager.process_borrow(
            self.hash_map, self.dll, self.user_array, "20211001", "B001", self.waiting_queue, borrow_date=date(2024, 1, 1)
        )
        self.assertFalse(success)

    def test_borrow_inactive_book(self):
        success, msg = loan_manager.process_borrow(
            self.hash_map, self.dll, self.user_array, "20211004", "B006", self.waiting_queue, borrow_date=date(2024, 1, 1)
        )
        self.assertFalse(success)

    def test_borrow_out_of_stock(self):
        success, msg = loan_manager.process_borrow(
            self.hash_map, self.dll, self.user_array, "20211004", "B007", self.waiting_queue, borrow_date=date(2024, 1, 1)
        )
        self.assertFalse(success)

    def test_borrow_custom_date(self):
        custom_date = date(2025, 1, 1)
        success, msg = loan_manager.process_borrow(
            self.hash_map, self.dll, self.user_array, "20211004", "B005", self.waiting_queue, borrow_date=custom_date
        )
        self.assertTrue(success)
        loan = self.dll.get_transactions_by_user("20211004")[0]
        self.assertEqual(loan.borrow_date, custom_date)
        self.assertEqual(loan.due_date, custom_date + timedelta(days=14))

    # ------------------------------------------------------------------ #
    # process_return
    # ------------------------------------------------------------------ #

    def test_return_no_overdue(self):
        loan = _find_loan(self.dll, "20211001", "L001")
        success, msg, fee = loan_manager.process_return(
            self.hash_map, self.dll, self.user_array, self.waiting_queue,
            "20211001", "B001", return_date=loan.due_date,
        )
        self.assertTrue(success)
        self.assertEqual(fee, 0.0)

    def test_return_with_overdue_fee(self):
        loan = _find_loan(self.dll, "20211001", "L001")
        return_date = loan.due_date + timedelta(days=3)
        success, msg, fee = loan_manager.process_return(
            self.hash_map, self.dll, self.user_array, self.waiting_queue,
            "20211001", "B001", return_date=return_date,
        )
        self.assertTrue(success)
        self.assertEqual(fee, 3 * 2000)

    def test_return_custom_date(self):
        loan = _find_loan(self.dll, "20211001", "L001")
        return_date = loan.due_date + timedelta(days=5)
        success, msg, fee = loan_manager.process_return(
            self.hash_map, self.dll, self.user_array, self.waiting_queue,
            "20211001", "B001", return_date=return_date,
        )
        self.assertTrue(success)
        self.assertEqual(fee, 5 * 2000)

    def test_return_loan_not_found(self):
        success, msg, fee = loan_manager.process_return(
            self.hash_map, self.dll, self.user_array, self.waiting_queue,
            "20211004", "B001", return_date=date(2024, 1, 1),
        )
        self.assertFalse(success)

    def test_return_priority_cascade_success(self):
        return_date = date(2024, 6, 1)
        success, msg, fee = loan_manager.process_return(
            self.hash_map, self.dll, self.user_array, self.waiting_queue,
            "20211001", "B001", return_date=return_date,
        )
        self.assertTrue(success)
        self.assertIsNone(_find_request(self.waiting_queue, "WR001"))
        self.assertEqual(self.waiting_queue.size, 2)
        u004_loans = self.dll.get_transactions_by_user("20211004")
        self.assertEqual(len(u004_loans), 1)
        self.assertEqual(u004_loans[0].status, "borrowing")
        self.assertEqual(u004_loans[0].borrow_date, return_date)

    def test_return_priority_cascade_ineligible(self):
        return_date = date(2024, 6, 1)
        success, msg, fee = loan_manager.process_return(
            self.hash_map, self.dll, self.user_array, self.waiting_queue,
            "20211003", "B003", return_date=return_date,
        )
        self.assertTrue(success)
        self.assertIsNotNone(_find_request(self.waiting_queue, "WR002"))
        self.assertEqual(self.waiting_queue.size, 3)
        u002_loans = self.dll.get_transactions_by_user("002.456.78901")
        self.assertEqual(len(u002_loans), 1)  # van chi co L002 cu, khong duoc muon them

    def test_return_priority_cascade_no_match(self):
        return_date = date(2024, 6, 1)
        success, msg, fee = loan_manager.process_return(
            self.hash_map, self.dll, self.user_array, self.waiting_queue,
            "20211003", "B002", return_date=return_date,
        )
        self.assertTrue(success)
        book = self.hash_map.search("B002")
        self.assertEqual(book.quantity, 4)  # 3 + 1, khong ai trong hang doi khop B002
        self.assertEqual(self.waiting_queue.size, 3)

    # ------------------------------------------------------------------ #
    # calculate_overdue_fee
    # ------------------------------------------------------------------ #

    def test_calculate_overdue_fee_not_due_yet(self):
        loan = _find_loan(self.dll, "20211001", "L001")
        user = self.user_array.get_by_id("20211001")
        fee = loan_manager.calculate_overdue_fee(loan, user, check_date=date(2024, 1, 1))
        self.assertEqual(fee, 0.0)

    def test_calculate_overdue_fee_overdue(self):
        loan = _find_loan(self.dll, "20211001", "L001")
        user = self.user_array.get_by_id("20211001")
        check_date = loan.due_date + timedelta(days=4)
        fee = loan_manager.calculate_overdue_fee(loan, user, check_date=check_date)
        self.assertEqual(fee, 4 * 2000)

    def test_calculate_overdue_fee_returned(self):
        loan = _find_loan(self.dll, "20211001", "L006")
        user = self.user_array.get_by_id("20211001")
        fee = loan_manager.calculate_overdue_fee(loan, user, check_date=date(2030, 1, 1))
        self.assertEqual(fee, 0.0)

    # ------------------------------------------------------------------ #
    # is_book_on_loan
    # ------------------------------------------------------------------ #

    def test_is_book_on_loan_true(self):
        self.assertTrue(loan_manager.is_book_on_loan(self.dll, "B001"))

    def test_is_book_on_loan_false(self):
        self.assertFalse(loan_manager.is_book_on_loan(self.dll, "B007"))

    # ------------------------------------------------------------------ #
    # add_to_waiting_queue
    # ------------------------------------------------------------------ #

    def test_add_to_waiting_queue_success(self):
        success, msg = loan_manager.add_to_waiting_queue(
            self.waiting_queue, "20211003", "B005", request_date=date(2024, 1, 1)
        )
        self.assertTrue(success)
        self.assertEqual(self.waiting_queue.size, 4)

    def test_add_to_waiting_queue_duplicate(self):
        success, msg = loan_manager.add_to_waiting_queue(
            self.waiting_queue, "20211004", "B001", request_date=date(2024, 1, 1)
        )
        self.assertFalse(success)
        self.assertEqual(self.waiting_queue.size, 3)

    def test_add_to_waiting_queue_custom_date(self):
        custom_date = date(2025, 5, 5)
        loan_manager.add_to_waiting_queue(self.waiting_queue, "002.456.78901", "B006", request_date=custom_date)
        new_request = _find_request(self.waiting_queue, "WR004")
        self.assertIsNotNone(new_request)
        self.assertEqual(new_request.request_date, custom_date)


if __name__ == "__main__":
    unittest.main()
